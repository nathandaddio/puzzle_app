from pyramid.exceptions import HTTPNotFound
from pyramid.view import view_config

from webargs.pyramidparser import use_kwargs

from marshmallow import fields


from puzzle_app.models import HitoriGameBoard

from puzzle_app.schemas.hitori import HitoriGameBoardSchema


@view_config(
    route_name='hitori_boards',
    request_method='GET',
    renderer='json'
)
def hitori_boards_get(request):
    db = request.db_session

    boards = db.query(HitoriGameBoard).all()

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
