import pytest
import mock

from puzzle_engine.hitori.models import (
    are_incompatible_cells,
    are_adjacent_cells,
    cell_incompatibility_factory,
    cell_adjacency_factory,
    cell_neighbourhood_factory,
    Board,
    Cell,
    CellAdjacency,
    CellNeighbourhood,
    CellIncompatibility,
    EngineData
)


def check_attributes(data, obj):
    for attribute, value in data.items():
        assert getattr(obj, attribute) == value


@pytest.fixture
def cell_values_1():
    return [
        [1, 3, 1],
        [3, 1, 2],
        [2, 3, 1],
    ]


@pytest.fixture
def cells_1(cell_values_1):
    return get_mock_cells_from_cell_values(cell_values_1)


@pytest.fixture
def expected_incompatibilities_cell_values_1():
    return set(
        [
            frozenset([(0, 0), (0, 2)]),
            frozenset([(0, 1), (2, 1)]),
            frozenset([(0, 2), (2, 2)]),
        ]
    )


@pytest.fixture
def expected_adjacencies_cell_values_1():
    return set(
        [
            frozenset([(0, 0), (0, 1)]),
            frozenset([(0, 0), (1, 0)]),
            frozenset([(0, 1), (0, 2)]),
            frozenset([(0, 1), (1, 1)]),
            frozenset([(0, 2), (1, 2)]),
            frozenset([(1, 0), (1, 1)]),
            frozenset([(1, 0), (2, 0)]),
            frozenset([(1, 1), (1, 2)]),
            frozenset([(1, 1), (2, 1)]),
            frozenset([(1, 2), (2, 2)]),
            frozenset([(2, 0), (2, 1)]),
            frozenset([(2, 1), (2, 2)])
        ]
    )


@pytest.fixture
def expected_cell_neighbourhoods_1():
    return set(
        [
            (
                (0, 0),
                frozenset([(0, 1), (1, 0)])
            ),
            (
                (0, 1),
                frozenset([(0, 0), (0, 2), (1, 1)])
            ),
            (
                (0, 2),
                frozenset([(0, 1), (1, 2)])
            ),
            (
                (1, 0),
                frozenset([(0, 0), (1, 1), (2, 0)])
            ),
            (
                (1, 1),
                frozenset([(1, 0), (0, 1), (1, 2), (2, 1)])
            ),
            (
                (1, 2),
                frozenset([(1, 1), (0, 2), (2, 2)])
            ),
            (
                (2, 0),
                frozenset([(1, 0), (2, 1)])
            ),
            (
                (2, 1),
                frozenset([(2, 0), (1, 1), (2, 2)])
            ),
            (
                (2, 2),
                frozenset([(2, 1), (1, 2)])
            )
        ]
    )


def get_mock_cells_from_cell_values(cell_values):
    return [
        mock.Mock(
            row_number=i,
            column_number=j,
            value=value,
            spec=['row_number', 'column_number', 'value']
        )
        for i, row in enumerate(cell_values)
        for j, value in enumerate(row)
    ]


class TestBoard:
    @pytest.fixture
    def id(self):
        return 1

    @pytest.fixture
    def number_of_rows(self):
        return 3

    @pytest.fixture
    def number_of_columns(self):
        return 3

    @pytest.fixture
    def values(self, cell_values_1):
        return cell_values_1

    @pytest.fixture
    def cells(self, values):
        return get_mock_cells_from_cell_values(values)

    @pytest.fixture
    def data(self, id, number_of_rows, number_of_columns, cells):
        return {
            'id': id,
            'number_of_rows': number_of_rows,
            'number_of_columns': number_of_columns,
            'cells': cells
        }

    @pytest.fixture
    def board(self, data):
        return Board(**data)

    def test_board_attributes(self, data, board):
        check_attributes(data, board)


class TestCell:
    @pytest.fixture
    def id(self):
        return 1

    @pytest.fixture
    def row_number(self):
        return 1

    @pytest.fixture
    def column_number(self):
        return 2

    @pytest.fixture
    def value(self):
        return 5

    @pytest.fixture
    def data(self, id, row_number, column_number, value):
        return {
            'id': id,
            'row_number': row_number,
            'column_number': column_number,
            'value': value
        }

    @pytest.fixture
    def cell(self, data):
        return Cell(**data)

    def test_cell_init(self, data, cell):
        check_attributes(data, cell)

    def test_cell_repr(self, data, cell):
        assert (
            repr(cell) ==
            "Cell(row={row_number},column={column_number},value={value})".format(**data)
        )


class TestEngineData:
    @pytest.fixture
    def board(self, cell_values_1):
        return mock.Mock(
            cells=get_mock_cells_from_cell_values(cell_values_1),
            number_of_rows=len(cell_values_1),
            number_of_columns=len(cell_values_1[0]),
            spec=['cells', 'number_of_rows', 'number_of_columns']
        )

    @pytest.fixture
    def data(self, board):
        return {
            'board': board
        }

    @pytest.fixture
    def engine_data(self, data):
        return EngineData(**data)

    def test_engine_data_attrs(self, data, engine_data):
        check_attributes(data, engine_data)

        other_attrs = ['cell_incompatibilities', 'cell_adjacencies']
        for attr in other_attrs:
            assert hasattr(engine_data, attr)


class TestCellIncompatibility:
    @pytest.fixture
    def cell_1(self):
        return mock.Mock()

    @pytest.fixture
    def cell_2(self):
        return mock.Mock()

    @pytest.fixture
    def cell_incompatability(self, cell_1, cell_2):
        return CellIncompatibility(cell_1, cell_2)

    def test_cell_incompatability_attrs(self, cell_1, cell_2, cell_incompatability):
        assert cell_incompatability.cell_1 == cell_1
        assert cell_incompatability.cell_2 == cell_2


CELL_SPEC = ['row_number', 'column_number', 'value']


def get_mock_cell(row_number, column_number, value):
    return mock.Mock(
        row_number=row_number,
        column_number=column_number,
        value=value,
        spec=CELL_SPEC
    )


class TestAreIncompatibleCells:
    cell_1_cell_2_incompatability = [
        (get_mock_cell(1, 2, 1), get_mock_cell(1, 3, 2), False),  # different values
        (get_mock_cell(1, 2, 1), get_mock_cell(1, 4, 2), False),  # different values
        (get_mock_cell(1, 2, 1), get_mock_cell(2, 4, 1), False),  # different row and column
        (get_mock_cell(2, 2, 1), get_mock_cell(2, 3, 1), True),  # same values, same row
        (get_mock_cell(1, 3, 1), get_mock_cell(2, 3, 1), True),  # same values, same column
    ]

    @pytest.mark.parametrize(['cell_1', 'cell_2', 'incompatible'], cell_1_cell_2_incompatability)
    def test_are_incompatible_cells(self, cell_1, cell_2, incompatible):
        assert are_incompatible_cells(cell_1, cell_2) == incompatible


class TestCellIncompatibilityFactory:
    @pytest.fixture
    def cells(self, cells_1):
        return cells_1

    @pytest.fixture
    def cell_incompatibilities(self, cells):
        return cell_incompatibility_factory(cells)

    def test_cell_incompatability_factory_gets_correct_cells(
            self, cell_incompatibilities, expected_incompatibilities_cell_values_1):
        assert expected_incompatibilities_cell_values_1 == set(
            [
                frozenset(
                    [
                        (incompat.cell_1.row_number, incompat.cell_1.column_number),
                        (incompat.cell_2.row_number, incompat.cell_2.column_number)
                    ]
                )
                for incompat in cell_incompatibilities
            ]
        )


class TestCellAdjacency:
    @pytest.fixture
    def cell_1(self):
        return mock.Mock()

    @pytest.fixture
    def cell_2(self):
        return mock.Mock()

    @pytest.fixture
    def cell_adjacency(self, cell_1, cell_2):
        return CellAdjacency(cell_1, cell_2)

    def test_cell_adjacency_attrs(self, cell_1, cell_2, cell_adjacency):
        assert cell_adjacency.cell_1 == cell_1
        assert cell_adjacency.cell_2 == cell_2


class TestAreAdjacentCells:
    cell_1_cell_2_adjacency = [
        (get_mock_cell(1, 2, 1), get_mock_cell(1, 3, 2), True),
        (get_mock_cell(1, 2, 1), get_mock_cell(1, 4, 2), False),
        (get_mock_cell(1, 2, 1), get_mock_cell(1, 1, 1), True),
        (get_mock_cell(3, 2, 1), get_mock_cell(3, 3, 1), True),
        (get_mock_cell(1, 3, 1), get_mock_cell(2, 3, 1), True),
        (get_mock_cell(0, 0, 1), get_mock_cell(5, 5, 1), False),
        (get_mock_cell(0, 0, 1), get_mock_cell(2, 0, 1), False),
        (get_mock_cell(0, 0, 1), get_mock_cell(0, 2, 1), False)
    ]

    @pytest.mark.parametrize(['cell_1', 'cell_2', 'adjacency'], cell_1_cell_2_adjacency)
    def test_are_adjacent_cells(self, cell_1, cell_2, adjacency):
        assert are_adjacent_cells(cell_1, cell_2) == adjacency


class TestCellAdjacencyFactory:
    @pytest.fixture
    def cells(self, cells_1):
        return cells_1

    @pytest.fixture
    def cell_adjacencies(self, cells):
        return cell_adjacency_factory(cells)

    def test_cell_adjacency_factory_gets_correct_cells(
            self, cell_adjacencies, expected_adjacencies_cell_values_1):
        assert expected_adjacencies_cell_values_1 == set(
            [
                frozenset(
                    [
                        (adjacency.cell_1.row_number, adjacency.cell_1.column_number),
                        (adjacency.cell_2.row_number, adjacency.cell_2.column_number)
                    ]
                )
                for adjacency in cell_adjacencies
            ]
        )


class TestCellNeighbourhood:
    @pytest.fixture
    def cell(self):
        return mock.Mock()

    @pytest.fixture
    def neighbours(self):
        return [mock.Mock(), mock.Mock(), mock.Mock()]

    @pytest.fixture
    def cell_neighbourhood(self, cell, neighbours):
        return CellNeighbourhood(cell, neighbours)

    def test_cell_neighbourhood_attrs(self, cell, cell_neighbourhood, neighbours):
        assert cell_neighbourhood.cell == cell
        assert cell_neighbourhood.neighbours == neighbours


class TestCellNeighbourhoodFactory:
    @pytest.fixture
    def cells(self, cells_1):
        return cells_1

    @pytest.fixture
    def cell_neighbourhoods(self, cells):
        return cell_neighbourhood_factory(cells)

    def test_cell_neighbourhood_factory_gets_cells(self, cell_neighbourhoods, expected_cell_neighbourhoods_1):
        assert expected_cell_neighbourhoods_1 == set(
            [
                (
                    (cell_neighbourhood.cell.row_number, cell_neighbourhood.cell.column_number),
                    frozenset((cell.row_number, cell.column_number) for cell in cell_neighbourhood.neighbours)
                )
                for cell_neighbourhood in cell_neighbourhoods
            ]
        )
