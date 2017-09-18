from collections import namedtuple

import transaction

from marshmallow import (
    fields,
    Schema,
    post_load
)


from puzzle_app.schemas.hitori import (
    HitoriGameBoardCellSchema,
    HitoriGameBoardSchema
)

from puzzle_app.models import (
    db_session_maker
)

from puzzle_app.models.hitori import (
    HitoriGameBoardCell,
    HitoriGameBoard,
    HitoriSolve,
    HITORI_SOLVE_STATUS
)


def make_hitori_engine_data(hitori_game_board_id):
    db_session = db_session_maker()
    hitori_game_board = db_session.query(HitoriGameBoard).get(hitori_game_board_id)
    return HitoriGameBoardSchema(strict=True).dump(hitori_game_board).data


HitoriSolution = namedtuple('HitoriSolution', ['board', 'cells_on', 'cells_off', 'feasible'])


def read_hitori_engine_data(hitori_engine_solution):
    solution = HitoriSolution(**hitori_engine_solution)

    with transaction.manager:
        db_session = db_session_maker()
        board = db_session.query(HitoriGameBoard).get(solution.board)

        board.solved = True
        board.feasible = solution.feasible

        for cell_id in solution.cells_on:
            db_session.query(HitoriGameBoardCell).get(cell_id).included_in_solution = True
        for cell_id in solution.cells_off:
            db_session.query(HitoriGameBoardCell).get(cell_id).included_in_solution = False


def update_hitori_solve_status(solve_id, status):
    with transaction.manager:
        db_session = db_session_maker()
        db_session.query(HitoriSolve).get(solve_id).status = HITORI_SOLVE_STATUS[status]
