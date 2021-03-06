import factory

import pytest


from puzzle_app.models import (
    HitoriGameBoard,
    HitoriGameBoardCell,
    HitoriSolve
)


class HitoriGameBoardFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HitoriGameBoard

    number_of_rows = 9
    number_of_columns = 9
    solved = False


class HitoriGameBoardCellFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HitoriGameBoardCell

    hitori_game_board = factory.SubFactory(HitoriGameBoardFactory)

    row_number = 5
    column_number = 3
    value = 3


class HitoriSolveFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = HitoriSolve

    hitori_game_board = factory.SubFactory(HitoriGameBoardFactory)


FACTORIES = [HitoriGameBoardFactory, HitoriGameBoardCellFactory, HitoriSolveFactory]
