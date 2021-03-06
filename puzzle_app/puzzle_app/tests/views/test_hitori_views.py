import pytest

from pyramid.exceptions import HTTPNotFound


from puzzle_app.views.hitori import hitori_boards_get, hitori_board_get


from factories import (
    HitoriGameBoardFactory,
    HitoriGameBoardCellFactory
)


class TestHitoriGameBoardsGet:
    @pytest.fixture
    def board(self, db_session):
        board = HitoriGameBoardFactory(number_of_rows=5, number_of_columns=5)

        db_session.add(board)
        db_session.commit()

        return board

    @pytest.fixture
    def cells(self, db_session, board):
        cells = [
            HitoriGameBoardCellFactory(hitori_game_board=board, row_number=3, column_number=4, value=6),
            HitoriGameBoardCellFactory(hitori_game_board=board, row_number=2, column_number=5, value=6)
        ]

        db_session.add_all(cells)
        db_session.commit()

        return cells

    @pytest.fixture
    def boards_response(self, dummy_request):
        return hitori_boards_get(dummy_request)

    @pytest.fixture
    def expected_boards_response(self, board, cells):
        return [
            {
                'id': board.id,
                'number_of_rows': board.number_of_rows,
                'number_of_columns': board.number_of_columns,
                'solved': False,
                'feasible': None,
                'cells': [  # note that the order of the cells changes as we return (row, column) order of cells
                    {
                        'id': cells[1].id,
                        'row_number': cells[1].row_number,
                        'column_number': cells[1].column_number,
                        'value': cells[1].value,
                        'included_in_solution': None
                    },
                    {
                        'id': cells[0].id,
                        'row_number': cells[0].row_number,
                        'column_number': cells[0].column_number,
                        'value': cells[0].value,
                        'included_in_solution': None
                    }
                ]
            }
        ]

    def test_hitori_game_boards_get(self, board, cells, boards_response, expected_boards_response):
        assert boards_response == expected_boards_response

    @pytest.fixture
    def board_request(self, board, dummy_request):
        dummy_request.matchdict['board_id'] = board.id
        return dummy_request

    @pytest.fixture
    def board_response(self, board_request):
        return hitori_board_get(board_request)

    def test_hitori_game_board_get(self, board, cells, board_response, expected_boards_response):
        assert board_response == expected_boards_response[0]

    @pytest.fixture
    def bad_board_id_request(self, dummy_request):
        dummy_request.matchdict['board_id'] = 100
        return dummy_request

    def test_board_get_bad_id(self, bad_board_id_request):
        with pytest.raises(HTTPNotFound):
            hitori_board_get(bad_board_id_request)
