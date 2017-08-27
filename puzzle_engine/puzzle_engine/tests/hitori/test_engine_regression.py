import pytest

from puzzle_engine.hitori.models import (
    Board,
    Cell,
    EngineData
)

from puzzle_engine.hitori.engine import HitoriEngine


class TestHitoriEngine:
    grids = [
        [
            [4, 8, 1, 6, 3, 2, 5, 7],
            [3, 6, 7, 2, 1, 6, 5, 4],
            [2, 3, 4, 8, 2, 8, 6, 1],
            [4, 1, 6, 5, 7, 7, 3, 5],
            [7, 2, 3, 1, 8, 5, 1, 2],
            [3, 5, 6, 7, 3, 1, 8, 4],
            [6, 4, 2, 3, 5, 4, 7, 8],
            [8, 7, 1, 4, 2, 3, 5, 6]
        ],
        [
            [12, 12, 4, 1, 11, 8, 10, 2, 3, 3, 11, 10],
            [6, 7, 3, 3, 5, 2, 11, 4, 9, 12, 5, 1],
            [8, 12, 9, 8, 6, 5, 3, 10, 2, 5, 2, 12],
            [10, 1, 1, 5, 5, 7, 8, 9, 3, 7, 6, 2],
            [6, 11, 2, 8, 2, 10, 8, 3, 10, 6, 9, 11],
            [3, 8, 12, 11, 8, 4, 2, 12, 6, 1, 5, 9],
            [9, 7, 3, 3, 11, 5, 11, 12, 5, 7, 4, 4],
            [5, 9, 9, 6, 7, 2, 1, 8, 2, 1, 4, 12],
            [11, 5, 8, 10, 7, 12, 9, 11, 5, 4, 7, 10],
            [8, 1, 1, 7, 8, 7, 10, 11, 9, 9, 11, 3],
            [1, 5, 2, 12, 2, 9, 7, 8, 10, 8, 3, 11],
            [7, 9, 6, 9, 1, 10, 4, 5, 6, 2, 10, 1],
        ],
        [
            [4, 2, 6, 3, 4, 5],
            [2, 5, 5, 5, 3, 5],
            [4, 5, 5, 2, 6, 1],
            [1, 3, 2, 1, 1, 2],
            [3, 3, 1, 4, 5, 2],
            [5, 1, 4, 5, 2, 4],
        ]

    ]

    solutions = [
        [
            (0, 0),
            (0, 2),
            (0, 6),
            (1, 5),
            (2, 0),
            (2, 3),
            (3, 2),
            (3, 5),
            (3, 7),
            (4, 1),
            (4, 3),
            (5, 0),
            (5, 4),
            (5, 7),
            (6, 1),
            (7, 4),
            (7, 6)
        ],
        [
            (0, 1),
            (0, 4),
            (0, 6),
            (0, 8),
            (1, 2),
            (1, 10),
            (2, 3),
            (2, 5),
            (2, 8),
            (2, 11),
            (3, 1),
            (3, 4),
            (3, 9),
            (4, 0),
            (4, 2),
            (4, 6),
            (4, 8),
            (4, 11),
            (5, 4),
            (5, 7),
            (6, 1),
            (6, 3),
            (6, 6),
            (6, 8),
            (6, 10),
            (7, 2),
            (7, 5),
            (7, 9),
            (8, 1),
            (8, 4),
            (8, 7),
            (8, 11),
            (9, 0),
            (9, 2),
            (9, 5),
            (9, 8),
            (9, 10),
            (10, 4),
            (10, 7),
            (11, 1),
            (11, 5),
            (11, 8),
            (11, 11)
        ],
        [
            (0, 0),
            (1, 1),
            (1, 3),
            (1, 5),
            (2, 2),
            (3, 0),
            (3, 3),
            (3, 5),
            (4, 1),
            (5, 3),
            (5, 5)
        ]
    ]

    grids_and_solutions = zip(grids, solutions)

    @pytest.fixture(params=grids_and_solutions)
    def grid_and_solution(self, request):
        return request.param

    @pytest.fixture()
    def grid(self, grid_and_solution):
        grid, _ = grid_and_solution
        return grid

    @pytest.fixture
    def expected_solution_cells_off_indexes(self, grid_and_solution):
        _, solution = grid_and_solution
        return set(solution)

    @pytest.fixture
    def cells(self, grid):
        return [
            Cell(i, j, val)
            for i, row in enumerate(grid)
            for j, val in enumerate(row)
        ]

    @pytest.fixture
    def board(self, grid, cells):
        return Board(
            number_of_rows=len(grid),
            number_of_columns=len(grid[0]),
            cells=cells
        )

    @pytest.fixture
    def engine_data(self, board):
        from puzzle_engine.hitori.schemas import BoardSchema
        import json

        with open('board.json', 'w') as board_fo:
            json.dump(BoardSchema().dump(board).data, board_fo)
        return EngineData(board)

    @pytest.fixture
    def engine(self, engine_data):
        return HitoriEngine(engine_data)

    @pytest.fixture
    def solution(self, engine):
        engine.solve()
        return engine.get_solution()

    def test_expected_solution(self, solution, expected_solution_cells_off_indexes):
        cells_off_indexes = [(cell.row_number, cell.column_number) for cell in solution.cells_off]

        assert set(cells_off_indexes) == expected_solution_cells_off_indexes
