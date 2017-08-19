import pytest
import mock


from puzzle_engine.hitori.engine import (
    AdjacentCellsConstraint,
    IncompatibleCellsConstraint,
    NeighbouringCellsConstraint,
    ComponentConstraint,
    get_cell_adjacencies_from_cells_on,
    get_neighbours_of_cells,
    gurobi_binary_variable_is_true
)


@pytest.fixture
def patch_quicksum_with_sum():
    """
    We have to do a little bit of dodgy quicksum
    patching with sum so we can test the logic of
    our constraints - quicksum returns a LinExpr,
    but we want an actual number
    """
    patcher = mock.patch('puzzle_engine.hitori.engine.quicksum', new=sum)
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def cells():
    return [
        mock.Mock(),
        mock.Mock(),
        mock.Mock(),
        mock.Mock()
    ]


class TestIncompatibleCellsConstraint:
    @pytest.fixture
    def cell_incompatibilities(self, cells):
        return [
            mock.Mock(cell_1=cells[0], cell_2=cells[1]),
            mock.Mock(cell_1=cells[1], cell_2=cells[2])
        ]

    @pytest.fixture
    def cell_on_variables(self, cells):
        return {
            cells[0]: False,
            cells[1]: True,
            cells[2]: True
        }

    @pytest.fixture
    def incompatible_cells_constraint(self, cell_on_variables):
        return IncompatibleCellsConstraint(cell_on_variables)

    def test_incompatible_cells_constraint_get_constraint(
            self, cell_incompatibilities, incompatible_cells_constraint):
        # cells 0 and 1 are incompatible, but only one is on, so this should return feasible
        assert incompatible_cells_constraint.get_constraint(cell_incompatibilities[0])

        # cells 1 and 2 are incompatible but both are on, so this should be infeasible
        assert not incompatible_cells_constraint.get_constraint(cell_incompatibilities[1])


class TestAdjacentCellsConstraint:
    @pytest.fixture
    def cell_adjacencies(self, cells):
        return [
            mock.Mock(cell_1=cells[0], cell_2=cells[1]),
            mock.Mock(cell_1=cells[1], cell_2=cells[2]),
            mock.Mock(cell_1=cells[0], cell_2=cells[2]),
            mock.Mock(cell_1=cells[2], cell_2=cells[3])
        ]

    @pytest.fixture
    def cell_on_variables(self, cells):
        return {
            cells[0]: False,
            cells[1]: False,
            cells[2]: True,
            cells[3]: True
        }

    @pytest.fixture
    def adjacent_cells_constraint(self, cell_on_variables):
        return AdjacentCellsConstraint(cell_on_variables)

    def test_adjacent_cells_constraint(self, cell_adjacencies, adjacent_cells_constraint):
        # Cell 0 and cell 1 are both off but adjacent
        assert not adjacent_cells_constraint.get_constraint(cell_adjacencies[0])

        # Cell 2 is on
        assert adjacent_cells_constraint.get_constraint(cell_adjacencies[1])

        # Cell 2 is on
        assert adjacent_cells_constraint.get_constraint(cell_adjacencies[2])

        # Cell 1 and cell 2 are both on
        assert adjacent_cells_constraint.get_constraint(cell_adjacencies[3])


class TestCellNeighbourhoodConstraint:
    @pytest.fixture
    def cell_neighbourhood(self, cells):
        return mock.Mock(cell=cells[0], neighbours=cells[1:])

    @pytest.fixture
    def cell_on_variables(self, cells):
        return {
            cell: False
            for cell in cells
        }

    @pytest.fixture
    def neighbouring_cells_constraint(self, cell_on_variables):
        return NeighbouringCellsConstraint(cell_on_variables)

    def test_neighbouring_cells_constraint_cell_not_on(
            self, cell_neighbourhood, cells, cell_on_variables, neighbouring_cells_constraint):
        # cell isn't on so should always be feasible (irrespective of neighbours)
        assert neighbouring_cells_constraint.get_constraint(cell_neighbourhood)

        # TODO: dodgy modification of these variables in place and DRY
        # Maybe parametrize this somehow
        cell_on_variables[cells[1]] = True
        assert neighbouring_cells_constraint.get_constraint(cell_neighbourhood)

        cell_on_variables[cells[2]] = True
        assert neighbouring_cells_constraint.get_constraint(cell_neighbourhood)

    def test_neighbouring_cells_constraint_cell_on(
            self, cell_neighbourhood, cells, cell_on_variables,
            neighbouring_cells_constraint, patch_quicksum_with_sum):
        cell_on_variables[cells[0]] = True
        assert not neighbouring_cells_constraint.get_constraint(cell_neighbourhood)

        cell_on_variables[cells[1]] = True
        assert neighbouring_cells_constraint.get_constraint(cell_neighbourhood)

        cell_on_variables[cells[3]] = True
        assert neighbouring_cells_constraint.get_constraint(cell_neighbourhood)


class TestComponentConstraint:
    @pytest.fixture
    def component(self, cells):
        return cells[:2]

    @pytest.fixture
    def component_neighbours(self, cells):
        return cells[2:3]

    @pytest.fixture
    def cell_on_variables(self, cells):
        return {
            cell: False
            for cell in cells
        }

    @pytest.fixture
    def component_constraint(self, cell_on_variables):
        return ComponentConstraint(cell_on_variables)

    cells_to_turn_on = [
        ([0, 1], False),  # having the same component should be infeasible
        ([0, 1, 2], True),  # adding in one of the neighbours should be feasible
        ([0, 1, 3], False)  # this cell is unrelated and so it should still be infeasible
    ]

    @pytest.mark.parametrize(["cell_indexes", "expected"], cells_to_turn_on)
    def test_component_constraint(
            self, component_constraint, patch_quicksum_with_sum,
            component, component_neighbours,
            cell_on_variables, cell_indexes, expected, cells):

        for cell_index in cell_indexes:
            cell_on_variables[cells[cell_index]] = True
        assert component_constraint.get_constraint(component, component_neighbours) is expected


class TestGetCellAdjacenciesFromCellsOn:
    @pytest.fixture
    def cells_on(self, cells):
        return cells[:3]

    @pytest.fixture
    def cell_adjacencies(self, cells):
        return [
            mock.Mock(cell_1=cells[0], cell_2=cells[1]),
            mock.Mock(cell_1=cells[1], cell_2=cells[2]),
            mock.Mock(cell_1=cells[2], cell_2=cells[3])
        ]

    @pytest.fixture
    def expected_cell_adjacencies(self, cells):
        return [(cells[0], cells[1]), (cells[1], cells[2])]

    def test_expected_cell_adjacencies(self, cells_on, cell_adjacencies,
            expected_cell_adjacencies):
        assert get_cell_adjacencies_from_cells_on(cells_on, cell_adjacencies) == expected_cell_adjacencies


class TestGetNeighboursOfCells:
    @pytest.fixture
    def cell_neighbours(self, cells):
        return [
            mock.Mock(
                cell=cells[0],
                neighbours=cells[1:2]
            ),
            mock.Mock(
                cell=cells[1],
                neighbours=[cells[0], cells[2]]
            ),
            mock.Mock(
                cell=cells[2],
                neighbours=cells[3:4]
            ),
        ]

    def test_get_neighbours_of_cells(self, cells, cell_neighbours):
        assert get_neighbours_of_cells(cells[0:1], cell_neighbours) == cells[1:2]
        assert get_neighbours_of_cells(cells[2:3], cell_neighbours) == cells[3:4]
        assert set(get_neighbours_of_cells([cells[0], cells[2]], cell_neighbours)) == set([cells[1], cells[3]])
        assert set(get_neighbours_of_cells(cells[0:3], cell_neighbours)) == set([cells[3]])
        assert get_neighbours_of_cells([cells[3]], cell_neighbours) == []
        assert get_neighbours_of_cells(cells, cell_neighbours) == []


class TestGurobiBinaryVariableIsTrue:
    @pytest.fixture
    def var(self):
        return mock.Mock()

    value_tolerance_expected = [
        (0, 0.001, False),
        (0.5, 0.001, False),
        (0.945, 0.001, False),
        (0.99, 0.001, False),
        (1.0, 0.001, True),
        (1.0, 0.0000001, True),
        (1.3, 0.01, False),
        (1.01, 0.001, False),
        (-1, 0.001, False),
        (0.99999, 0.001, True),
        (0.51, 0.001, False)
    ]

    def get_value_getter(self, value):
        return lambda x: value

    @pytest.mark.parametrize(['value', 'tolerance', 'expected'], value_tolerance_expected)
    def test_gurobi_binary_variable_is_true(self, var, value, tolerance, expected):
        value_getter = self.get_value_getter(value)

        assert gurobi_binary_variable_is_true(
            var, value_getter=value_getter, tolerance=tolerance) is expected

    @pytest.fixture
    def value_getter(self):
        val_getter = mock.Mock()
        val_getter.return_value = 1
        return val_getter

    def test_value_getter_is_called_with_var(self, var, value_getter):
        gurobi_binary_variable_is_true(var, value_getter)

        value_getter.assert_called_once_with(var)
