import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from puzzle_app.models.meta import Base
from puzzle_app.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )


from puzzle_app.models import HitoriGameBoard, HitoriGameBoardCell


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


hitori_game_board = [
    [12, 12, 4, 1, 11, 8, 10, 2, 3, 3, 11, 10],
    [6, 7, 3, 3, 5, 2, 11, 4, 9, 12, 5, 1],
    [8, 12, 9, 8, 6, 5, 3, 10, 2, 5, 2, 12],
    [10, 1, 1, 5, 5, 7, 8, 9, 3, 7, 6, 2],
    [6, 11, 2, 8, 2, 10, 8, 3, 10, 6, 9, 11],
    [3, 8, 12, 11, 8, 4, 2, 12, 6, 1, 5, 9],
    [9, 7, 3, 3, 11, 5, 11, 12, 5, 7, 4, 4],
    [5, 9, 9, 6, 7, 2, 1, 8, 2, 1, 4, 12],
    [11, 5, 8, 10, 7, 12, 9, 11, 5, 4, 7, 10],
    [8, 1, 1, 7, 8, 7, 10, 11, 9, 9, 11, 3],
    [1, 5, 2, 12, 2, 9, 7, 8, 10, 8, 3, 11],
    [7, 9, 6, 9, 1, 10, 4, 5, 6, 2, 10, 1],
]


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        board = HitoriGameBoard(number_of_rows=len(hitori_game_board), number_of_columns=len(hitori_game_board))
        cells = [
            HitoriGameBoardCell(hitori_game_board=board, row_number=i, column_number=j, value=value)
            for i, row in enumerate(hitori_game_board)
            for j, value in enumerate(row)
        ]
        dbsession.add(board)
        dbsession.add_all(cells)


if __name__ == "__main__":
    main()
