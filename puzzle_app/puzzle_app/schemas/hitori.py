from marshmallow import (
    fields,
    Schema,
    post_dump,
    validate
)


from marshmallow_enum import EnumField

from puzzle_app.models import HITORI_SOLVE_STATUS


nonnegative = validate.Range(min=0)


class HitoriGameBoardCellSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(required=True, validate=nonnegative)

    row_number = fields.Int(required=True, validate=nonnegative)
    column_number = fields.Int(required=True, validate=nonnegative)

    value = fields.Int(required=True, validate=nonnegative)

    included_in_solution = fields.Bool(allow_none=True)


class HitoriGameBoardSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int()

    number_of_rows = fields.Int(required=True)
    number_of_columns = fields.Int(required=True)

    cells = fields.Nested(HitoriGameBoardCellSchema, many=True, required=True)

    solved = fields.Bool(allow_none=True)

    feasible = fields.Bool(allow_none=True)

    @post_dump
    def order_cells(self, data):
        data['cells'] = sorted(data['cells'], key=lambda cell: (cell['row_number'], cell['column_number']))
        return data


class HitoriSolveSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Int(required=True)

    started_at = fields.DateTime(required=True)
    status = EnumField(HITORI_SOLVE_STATUS, required=True)
    hitori_game_board_id = fields.Int(required=True)
