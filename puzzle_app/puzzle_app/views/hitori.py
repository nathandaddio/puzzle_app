from pyramid.exceptions import HTTPNotFound
from pyramid.view import view_config

from webargs.pyramidparser import use_kwargs

from marshmallow import fields


from puzzle_app.models import HitoriGameBoard, HitoriSolve, clone_hitori_game_board, HitoriGameBoardCell

from puzzle_app.schemas.hitori import HitoriGameBoardSchema, HitoriSolveSchema, HitoriGameBoardCellSchema


from puzzle_app.jobs import get_hitori_solve_chain, hitori_solve, hitori_engine_input


@view_config(
    route_name='hitori_boards',
    request_method='GET',
    renderer='json'
)
def hitori_boards_get(request):
    db = request.db_session

    boards = db.query(HitoriGameBoard).order_by(HitoriGameBoard.id.desc()).all()

    schema = HitoriGameBoardSchema(strict=True, many=True)

    result = schema.dump(boards)

    return result.data


@view_config(
    route_name='hitori_board',
    request_method='GET',
    renderer='json'
)
@use_kwargs({'board_id': fields.Int(required=True, location='matchdict')})
def hitori_board_get(request, board_id):
    db_session = request.db_session

    board = db_session.query(HitoriGameBoard).get(board_id)

    if board is None:
        raise HTTPNotFound("Board with ID {} not found".format(board_id))

    schema = HitoriGameBoardSchema(strict=True)

    return schema.dump(board).data


@view_config(
    route_name='hitori_boards',
    request_method='POST',
    renderer='json'
)
def hitori_board_post(request):
    db_session = request.db_session

    json_data = request.json_body

    json_data['cells'] = []

    data = HitoriGameBoardSchema(strict=True).load(json_data).data

    board = HitoriGameBoard(**data)

    cells = [
        HitoriGameBoardCell(hitori_game_board=board, row_number=i, column_number=j)
        for i in range(board.number_of_rows)
        for j in range(board.number_of_columns)
    ]

    db_session.add(board)
    db_session.add_all(cells)

    db_session.flush()

    return HitoriGameBoardSchema(strict=True).dump(board).data


@view_config(
    route_name='hitori_board_clone',
    request_method='POST',
    renderer='json'
)
@use_kwargs({'board_id': fields.Int(required=True, location='matchdict')})
def hitori_board_clone(request, board_id):
    db_session = request.db_session

    board = db_session.query(HitoriGameBoard).get(board_id)

    new_board = clone_hitori_game_board(db_session, board)

    db_session.flush()

    return {'id': new_board.id}


@view_config(
    route_name='hitori_board_solve',
    request_method='GET',
    renderer='json'
)
@use_kwargs({'board_id': fields.Int(required=True, location='matchdict')})
def hitori_board_solve(request, board_id):
    db_session = request.db_session

    board = db_session.query(HitoriGameBoard).get(board_id)
    solve = HitoriSolve(hitori_game_board=board)
    db_session.add(solve)
    db_session.flush()

    get_hitori_solve_chain(board_id, solve.id)()
    return {'solve_id': solve.id}


@view_config(
    route_name='hitori_cell_value',
    request_method='POST',
    renderer='json'
)
@use_kwargs({'cell_id': fields.Int(required=True, location='matchdict')})
def hitori_cell_value_update(request, cell_id):
    db_session = request.db_session

    cell = db_session.query(HitoriGameBoardCell).get(cell_id)

    value = request.json_body['value']

    cell.value = value

    db_session.flush()

    return HitoriGameBoardCellSchema().dump(cell).data


@view_config(
    route_name='hitori_solves',
    request_method='GET',
    renderer='json'
)
def hitori_solves_get(request):
    db = request.db_session
    solves = db.query(HitoriSolve).all()
    schema = HitoriSolveSchema(strict=True, many=True)
    return schema.dump(solves).data


@view_config(
    route_name='hitori_solve',
    request_method='GET',
    renderer='json'
)
@use_kwargs({'solve_id': fields.Int(required=True, location='matchdict')})
def hitori_solve_get(request, solve_id):
    db = request.db_session
    solve = db.query(HitoriSolve).get(solve_id)
    schema = HitoriSolveSchema(strict=True)
    return schema.dump(solve).data
