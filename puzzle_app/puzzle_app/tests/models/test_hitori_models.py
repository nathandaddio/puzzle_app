import pytest

from sqlalchemy import inspect

from puzzle_app.models.hitori import (
    HitoriGameBoard,
    HitoriGameBoardCell
)

from factories import (
    HitoriGameBoardFactory,
    HitoriGameBoardCellFactory,
)


class TestHitoriGameBoard:
    @pytest.fixture
    def game_board(self, db_session):
        game_board = HitoriGameBoardFactory()

        db_session.add(game_board)
        db_session.commit()

        return game_board

    def test_hitori_game_board_init(self, game_board):
        assert game_board

    def test_hitori_game_board_attrs(self, game_board):
        attrs = ['id', 'cells', 'number_of_rows', 'number_of_columns', 'solved']
        for attr in attrs:
            assert hasattr(game_board, attr)

    def test_hitori_game_board_init_with_no_cells(self, game_board):
        assert list(game_board.cells) == []

    def test_hitori_game_board_added_to_db(self, db_session, game_board):
        db_game_boards = db_session.query(HitoriGameBoard).all()

        assert db_game_boards

        assert len(db_game_boards) == 1

        db_game_board = db_game_boards[0]

        assert db_game_board == game_board


class TestHitoriGameBoardCell:
    @pytest.fixture
    def row_number(self):
        return 3

    @pytest.fixture
    def column_number(self):
        return 2

    @pytest.fixture
    def value(self):
        return 5

    @pytest.fixture
    def cell(self, db_session, row_number, column_number, value):
        cell = HitoriGameBoardCellFactory(
            row_number=row_number, column_number=column_number, value=value)

        db_session.add(cell)
        db_session.commit()

        return cell

    def test_hitori_game_board_cell_init(self, cell):
        assert cell.row_number == 3
        assert cell.column_number == 2
        assert cell.value == 5
        assert cell.hitori_game_board

    def test_hitori_game_board_cell_added_to_db(self, db_session, cell):
        db_cells = db_session.query(HitoriGameBoardCell).all()

        assert db_cells

        assert len(db_cells) == 1

        assert db_cells[0] == cell

    def test_hitori_game_board_included_in_solution_is_none_on_init(self, cell):
        assert cell.included_in_solution is None


class TestBoardCellRelationship:
    @pytest.fixture
    def board(self, db_session):
        board = HitoriGameBoardFactory()

        db_session.add(board)
        db_session.commit()

        return board

    @pytest.fixture
    def cell(self, db_session, board):
        cell = HitoriGameBoardCellFactory(hitori_game_board=board)

        db_session.add(cell)
        db_session.commit()

        return cell

    def test_cell_to_board_relationship(self, board, cell):
        assert cell.hitori_game_board_id == board.id

        assert cell.hitori_game_board == board

    def test_board_to_cells_relationship(self, board, cell):
        assert board.cells
        assert len(board.cells) == 1

        assert board.cells[0] == cell

    def test_deleting_board_deletes_cells(self, db_session, board, cell):
        db_session.delete(board)
        db_session.commit()

        assert db_session.query(HitoriGameBoard).all() == []
        assert db_session.query(HitoriGameBoardCell).all() == []

        board_insp = inspect(board)
        assert board_insp.detached

        cell_insp = inspect(cell)
        assert cell_insp.detached

    def test_deleting_cell_does_not_delete_board(self, db_session, board, cell):
        db_session.delete(cell)
        db_session.commit()

        assert db_session.query(HitoriGameBoard).all() == [board]

        assert db_session.query(HitoriGameBoardCell).all() == []

        assert inspect(board).persistent

        assert inspect(cell).detached
