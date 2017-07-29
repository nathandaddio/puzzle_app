import pytest

from puzzle_app.models.hitori import (
    HitoriGameBoard,
    HitoriGameBoardCell
)

from factories import (
    HitoriGameBoardFactory,
    HitoriGameBoardCellFactory,
)


from puzzle_app.views.hitori import hitori_boards_get


def test_hitori_game_board_init(db_session):
    game_board = HitoriGameBoardFactory()

    attrs = ['id', 'cells']
    for attr in attrs:
        assert hasattr(game_board, attr)

    assert list(game_board.cells) == []


def test_hitori_game_board_cell_init(db_session):
    cell = HitoriGameBoardCellFactory(row_number=3, column_number=2, value=5)

    assert cell.row_number == 3
    assert cell.column_number == 2
    assert cell.value == 5
    assert cell.hitori_game_board

    assert cell in cell.hitori_game_board.cells


def test_hitori_game_board_cell_backrefs(db_session):
    board = HitoriGameBoardFactory()
    cell = HitoriGameBoardCellFactory(hitori_game_board=board)

    assert cell.hitori_game_board_id == board.id


def test_hitori_game_board_cell_not_included_in_solution_on_init(db_session):
    cell = HitoriGameBoardCellFactory()

    assert cell.included_in_solution is None


def test_hitori_game_board_ondelete(db_session):
    game_board = HitoriGameBoardFactory()

    cell = HitoriGameBoardCellFactory(hitori_game_board=game_board)

    assert cell.hitori_game_board is game_board

    db_session.commit()

    assert db_session.query(HitoriGameBoard).all() == [game_board]
    assert db_session.query(HitoriGameBoardCell).all() == [cell]

    db_session.delete(game_board)
    db_session.commit()

    assert db_session.query(HitoriGameBoard).all() == []
    assert db_session.query(HitoriGameBoardCell).all() == []


def test_hitori_game_board_cell_ondelete(db_session):
    game_board = HitoriGameBoardFactory()
    cell = HitoriGameBoardCellFactory(hitori_game_board=game_board)

    db_session.commit()

    assert db_session.query(HitoriGameBoard).all() == [game_board]
    assert db_session.query(HitoriGameBoardCell).all() == [cell]

    db_session.delete(cell)
    db_session.commit()

    assert db_session.query(HitoriGameBoard).all() == [game_board]
    assert db_session.query(HitoriGameBoardCell).all() == []


def test_hitori_game_board_get(dummy_request, db_session):
    game_board = HitoriGameBoardFactory(number_of_rows=5, number_of_columns=5)
    cell = HitoriGameBoardCellFactory(hitori_game_board=game_board, row_number=3, column_number=4, value=6)
    db_session.commit()

    response = hitori_boards_get(dummy_request)

    assert len(response) == 1

    game_board_json = response[0]
    assert game_board_json['id'] == game_board.id
    assert game_board_json['number_of_rows'] == game_board.number_of_rows
    assert game_board_json['number_of_columns'] == game_board.number_of_columns
    assert len(game_board_json['cells']) == 1

    cell_json = game_board_json['cells'][0]
    assert cell_json['id'] == cell.id
    assert cell_json['row_number'] == cell.row_number
    assert cell_json['column_number'] == cell.column_number
    assert cell_json['value'] == cell.value
    assert cell_json['included_in_solution'] is None
