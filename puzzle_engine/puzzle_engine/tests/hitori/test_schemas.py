import pytest
import mock


from marshmallow import ValidationError


from puzzle_engine.hitori.schemas import (
    CellSchema,
    BoardSchema,
    HitoriSolutionSchema
)


class TestCellSchema:
    @pytest.fixture
    def data(self):
        return {
            'row_number': 1,
            'column_number': 2,
            'value': 5
        }

    @pytest.fixture
    def patched_cell(self):
        patcher = mock.patch('puzzle_engine.hitori.schemas.Cell')
        yield patcher.start()
        patcher.stop()

    def test_cell_schema_loads(self, data, patched_cell):
        loaded_data = CellSchema(strict=True).load(data).data

        assert loaded_data is patched_cell.return_value
        patched_cell.assert_called_once_with(**data)

    bad_data = [
        {
            'row_number': 3,
            'column_number': -1,
            'value': 5
        },
        {
            'row_number': -3,
            'column_number': 5,
            'value': 5
        },
        {
            'row_number': -3,
            'column_number': -5,
            'value': 2
        }
    ]

    @pytest.mark.parametrize('data', bad_data)
    def test_cell_schema_validates(self, data):
        with pytest.raises(ValidationError):
            CellSchema(strict=True).load(data)


class TestBoardSchema:
    @pytest.fixture
    def data(self):
        return {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 1,
                    'column_number': 2,
                    'value': 3
                }
            ]
        }

    @pytest.fixture
    def patched_board(self):
        patcher = mock.patch('puzzle_engine.hitori.schemas.Board')
        yield patcher.start()
        patcher.stop()

    def test_board_schema_loads(self, data, patched_board):
        loaded_data = BoardSchema(strict=True).load(data).data

        assert patched_board.return_value is loaded_data

        call = patched_board.call_args[1]
        assert call['number_of_rows'] == data['number_of_rows']
        assert call['number_of_columns'] == data['number_of_columns']

        assert call['cells']
        assert len(call['cells']) == 1

        cell = call['cells'][0]

        assert cell.row_number == 1
        assert cell.column_number == 2
        assert cell.value == 3

    bad_data = [
        {
            'number_of_rows': -5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 1,
                    'column_number': 2,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': -5,
            'cells': [
                {
                    'row_number': 1,
                    'column_number': 2,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': -5,
            'number_of_columns': -5,
            'cells': [
                {
                    'row_number': 1,
                    'column_number': 2,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 10,
                    'column_number': 2,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 3,
                    'column_number': 12,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 10,
                    'column_number': 12,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 1,
                    'column_number': 6,
                    'value': 3
                },
                {
                    'row_number': 3,
                    'column_number': 2,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 5,
                    'column_number': 3,
                    'value': 3
                }
            ]
        },
        {
            'number_of_rows': 5,
            'number_of_columns': 5,
            'cells': [
                {
                    'row_number': 3,
                    'column_number': 5,
                    'value': 3
                }
            ]
        },
    ]

    @pytest.mark.parametrize('data', bad_data)
    def test_board_schema_validates(self, data):
        with pytest.raises(ValidationError):
            BoardSchema(strict=True).load(data)


class TestHitoriSolutionSchema:
    @pytest.fixture
    def cells_on(self):
        return [
            {
                'row_number': 1,
                'column_number': 2,
                'value': 2
            },
            {
                'row_number': 2,
                'column_number': 3,
                'value': 5
            }
        ]

    @pytest.fixture
    def cells_off(self):
        return [
            {
                'row_number': 5,
                'column_number': 2,
                'value': 1
            }
        ]

    @pytest.fixture
    def hitori_solution(self, cells_on, cells_off):
        return {
            'cells_on': cells_on,
            'cells_off': cells_off
        }

    def test_hitori_solution_schema_dump(self, hitori_solution):
        data = HitoriSolutionSchema(strict=True).dump(hitori_solution).data
        assert data == hitori_solution
