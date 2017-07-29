from pyramid.response import Response
from pyramid.view import view_config


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
