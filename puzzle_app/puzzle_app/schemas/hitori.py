from marshmallow import (
    fields,
    Schema,
)


class HitoriGameBoardCellSchema(Schema):
    id = fields.Int(required=True)

    row_number = fields.Int(required=True)
    column_number = fields.Int(required=True)

    value = fields.Int(required=True)

    included_in_solution = fields.Bool(allow_none=True)


class HitoriGameBoardSchema(Schema):
    id = fields.Int(required=True)

    number_of_rows = fields.Int(required=True)
    number_of_columns = fields.Int(required=True)

    cells = fields.Nested(HitoriGameBoardCellSchema, many=True, required=True)

    solved = fields.Bool(allow_none=True)
