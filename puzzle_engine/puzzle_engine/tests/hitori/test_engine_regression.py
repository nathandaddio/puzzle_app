import pytest

from puzzle_engine.hitori.models import (Board, Cell, EngineData)

from puzzle_engine.hitori.engine import HitoriEngine


class TestHitoriEngineOnSimpleDataset:
    @pytest.fixture
    def grid(self):
        return [
            [4, 8, 1, 6, 3, 2, 5, 7],
            [3, 6, 7, 2, 1, 6, 5, 4],
            [2, 3, 4, 8, 2, 8, 6, 1],
            [4, 1, 6, 5, 7, 7, 3, 5],
            [7, 2, 3, 1, 8, 5, 1, 2],
            [3, 5, 6, 7, 3, 1, 8, 4],
            [6, 4, 2, 3, 5, 4, 7, 8],
            [8, 7, 1, 4, 2, 3, 5, 6]
        ]

    @pytest.fixture
    def expected_solution_cells_off_indexes(self):
        return set(
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
            ]
        )

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
