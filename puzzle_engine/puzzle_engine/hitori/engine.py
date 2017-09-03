import logging


from gurobipy import (
    GRB,
    Model,
    quicksum,
)


from networkx import Graph, connected_components


logger = logging.getLogger(__name__)


def hitori_solve(engine_data):
    engine = HitoriEngine(engine_data)
    engine.solve()
    return engine.get_solution()


class HitoriEngine(object):
    def __init__(self, engine_data):
        self._engine_data = engine_data

        self._model = Model()
        self._model.params.lazyConstraints = True

        self._formulate()

    def _formulate(self):
        self._variables = HitoriEngineVariables(self._engine_data, self._model)
        self._objective = HitoriEngineObjective(self._engine_data, self._model, self._variables)
        self._constraints = HitoriEngineConstraints(self._engine_data, self._model, self._variables)

    def solve(self):
        callback_handler = HitoriEngineCallback(self._engine_data, self._variables)

        def unbound_callback(model, where):  # bit of a hack to appease gurobi
            return callback_handler.callback(model, where)

        self._model.optimize(unbound_callback)

    def get_solution(self):
        solution_adapter = HitoriEngineSolutionAdapter(self._engine_data, self._model, self._variables)
        return solution_adapter.get_solution()


class HitoriEngineVariables(object):
    def __init__(self, engine_data, model):
        self._engine_data = engine_data
        self._board = self._engine_data.board
        self._model = model

        self.cell_on = self._add_cell_on_variables()

        self._model.update()

    def _add_cell_on_variables(self):
        return {
            cell:
                self._model.addVar(
                    vtype=GRB.BINARY,
                    name="cell_on_{}".format(cell)
                )
            for cell in self._board.cells
        }


class HitoriEngineObjective(object):
    def __init__(self, engine_data, model, variables):
        self._engine_data = engine_data
        self._model = model
        self._variables = variables

        self._set_objective()

    def _set_objective(self):
        obj = quicksum(cell_on for cell_on in self._variables.cell_on.values())
        self._model.setObjective(obj, GRB.MAXIMIZE)


class HitoriEngineConstraints(object):
    def __init__(self, engine_data, model, variables):
        self._engine_data = engine_data
        self._model = model
        self._variables = variables

        self.incompatible_cells_constraints = self._add_incompatible_cells_constraints()
        self.adjacent_cells_constraints = self._add_adjacent_cells_constraints()
        self.neighbouring_cells_constraints = self._add_neighbouring_cells_constraints()

    def _add_incompatible_cells_constraints(self):
        constraint_generator = IncompatibleCellsConstraint(self._variables.cell_on)
        return {
            cell_incompatibility:
                self._model.addConstr(
                    constraint_generator.get_constraint(cell_incompatibility),
                    name="incompatible_cells_{}".format(cell_incompatibility)
                )
            for cell_incompatibility in self._engine_data.cell_incompatibilities
        }

    def _add_adjacent_cells_constraints(self):
        constraint_generator = AdjacentCellsConstraint(self._variables.cell_on)

        return {
            adjacent_cells:
                self._model.addConstr(
                    constraint_generator.get_constraint(adjacent_cells),
                    name="adjacent_cells_{}".format(adjacent_cells)
                )
            for adjacent_cells in self._engine_data.cell_adjacencies
        }

    def _add_neighbouring_cells_constraints(self):
        constraint_generator = NeighbouringCellsConstraint(self._variables.cell_on)

        return {
            neighbourhood:
                self._model.addConstr(
                    constraint_generator.get_constraint(neighbourhood),
                    name="neighbourhood_{}".format(neighbourhood)
                )
            for neighbourhood in self._engine_data.cell_neighbourhoods
        }


class IncompatibleCellsConstraint(object):
    """Two incompatible cells cannot simultaneously be on"""
    def __init__(self, cell_on):
        self._cell_on = cell_on

    def get_constraint(self, cell_incompatibility):
        return (
            self._cell_on[cell_incompatibility.cell_1] +
            self._cell_on[cell_incompatibility.cell_2] <= 1
        )


class AdjacentCellsConstraint(object):
    """For every pair of adjacent cells, at least one must be on"""
    def __init__(self, cell_on):
        self._cell_on = cell_on

    def get_constraint(self, adjacent_cells):
        return (
            self._cell_on[adjacent_cells.cell_1] +
            self._cell_on[adjacent_cells.cell_2] >= 1
        )


class NeighbouringCellsConstraint(object):
    """If a cell is on, one of its neighbours must be on"""
    def __init__(self, cell_on):
        self._cell_on = cell_on

    def get_constraint(self, cell_neighbourhood):
        return (
            self._cell_on[cell_neighbourhood.cell] <=
            quicksum(self._cell_on[cell] for cell in cell_neighbourhood.neighbours)
        )


class ComponentConstraint(object):
    """
    For each possible component in the graph of the board,
    it's either not in the solution, or one of its neighbours is on.

    Note: the number of possible components is exponential, so this is
    a lazy constraint.
    """
    def __init__(self, cell_on):
        self._cell_on = cell_on

    def get_constraint(self, component, component_neighbours):
        return (
            quicksum(1 - self._cell_on[cell] for cell in component) +
            quicksum(self._cell_on[cell] for cell in component_neighbours) >= 1
        )


class HitoriEngineSolutionAdapter(object):
    def __init__(self, engine_data, model, variables):
        self._model = model
        self._variables = variables
        self._engine_data = engine_data

    def get_solution(self):
        return HitoriSolution(
            cells_on=[
                cell
                for cell, var in self._variables.cell_on.items()
                if gurobi_binary_variable_is_true(var)
            ],
            cells_off=[
                cell
                for cell, var in self._variables.cell_on.items()
                if not gurobi_binary_variable_is_true(var)
            ],
            board=self._engine_data.board
        )


class HitoriSolution(object):
    def __init__(self, cells_on, cells_off, board):
        self.cells_on = cells_on
        self.cells_off = cells_off
        self.board = board


class HitoriEngineCallback(object):
    def __init__(self, engine_data, variables):
        self._engine_data = engine_data
        self._variables = variables

        self._connectivity_callback = ConnectivityCallback(self._engine_data, self._variables)

    def callback(self, model, where):
        if where == GRB.Callback.MIPSOL:
            cells_on = self._get_cells_on(model)
            self._connectivity_callback.callback(model, cells_on)

    def _get_cells_on(self, model):
        return [
            cell
            for cell, var in self._variables.cell_on.items()
            if gurobi_binary_variable_is_true(var, value_getter=model.cbGetSolution)
        ]


class ConnectivityCallback(object):
    def __init__(self, engine_data, variables):
        self._engine_data = engine_data
        self._variables = variables

        self._connected_component_constraint_generator = ComponentConstraint(self._variables.cell_on)

    def callback(self, model, cells_on):
        """
        Finds the smallest connected component (if it exists)
        of the graph of the solution and adds a lazy cut to
        force the graph to become connected.
        """
        components = get_connected_components_from_cells_on(cells_on, self._engine_data.cell_adjacencies)

        if len(components) == 1:  # if this is true, then we've found a solution!
            return

        component = get_smallest_component(components)
        self._remove_component(model, component)

    def _remove_component(self, model, component):
        logger.debug("Cutting component %s", component)

        component_neighbours = get_neighbours_of_cells(component, self._engine_data.cell_neighbourhoods)

        logger.debug("Component has neighbours %s", component_neighbours)

        model.cbLazy(self._connected_component_constraint_generator.get_constraint(component, component_neighbours))


def get_connected_components_from_cells_on(cells_on, cell_adjacencies):
    graph = get_graph_from_cells_on(cells_on, cell_adjacencies)
    return list(connected_components(graph))


def get_smallest_component(components):
    return min(components, key=len)


def get_graph_from_cells_on(cells_on, cell_adjacencies):
    graph = Graph()
    graph.add_nodes_from(cells_on)
    graph.add_edges_from(get_cell_adjacencies_from_cells_on(cells_on, cell_adjacencies))
    return graph


def get_cell_adjacencies_from_cells_on(cells_on, cell_adjacencies):
    cells_on = set(cells_on)
    return [
        (cell_adjacency.cell_1, cell_adjacency.cell_2)
        for cell_adjacency in cell_adjacencies
        if cell_adjacency.cell_1 in cells_on
        and cell_adjacency.cell_2 in cells_on
    ]


def get_neighbours_of_cells(cells, cell_neighbourhoods):
    cells = set(cells)
    return [
        nbr
        for cell_neighbourhood in cell_neighbourhoods
        for nbr in cell_neighbourhood.neighbours
        if cell_neighbourhood.cell in cells and
        nbr not in cells
    ]


def gurobi_binary_variable_is_true(var, value_getter=lambda var: var.x, tolerance=10**(-5)):
    return abs(value_getter(var) - 1) < tolerance
