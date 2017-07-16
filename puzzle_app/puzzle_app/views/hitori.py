from pyramid.response import Response
from pyramid.view import view_config


from puzzle_app.models import HitoriGameBoard


@view_config(
    route_name='hitori_boards',
    request_method='GET',
    renderer='json'
)
def hitori_boards_get(request):
    db = request.db_session

    boards = db.query(HitoriGameBoard).all()

    return [
        {
            'board_id': board.id,
            'number_of_rows': board.number_of_rows,
            'number_of_columns': board.number_of_columns,
            'cells': [
                {
                    'cell_id': cell.id,
                    'row_number': cell.row_number,
                    'column_number': cell.column_number,
                    'value': cell.value,
                    'included_in_solution': cell.included_in_solution
                }
                for cell in board.cells
            ]
        }
        for board in boards
    ]
