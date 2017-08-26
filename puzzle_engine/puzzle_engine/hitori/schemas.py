from marshmallow import (
    Schema,
    fields,
    validate,
    post_load,
    validates_schema,
    ValidationError
)

from puzzle_engine.hitori.models import (
    Board,
    Cell
)


nonnegative = validate.Range(min=0)


class CellSchema(Schema):
    row_number = fields.Int(required=True, validate=nonnegative)
    column_number = fields.Int(required=True, validate=nonnegative)
    value = fields.Int(required=True)

    @post_load
    def load_cell(self, data):
        return Cell(**data)


class BoardSchema(Schema):
    number_of_rows = fields.Int(required=True, validate=nonnegative)
    number_of_columns = fields.Int(required=True, validate=nonnegative)
    cells = fields.Nested(CellSchema, many=True, required=True)

    @post_load
    def load_board(self, data):
        return Board(**data)

    @validates_schema(skip_on_field_errors=True)
    def check_cells_are_within_bounds(self, data):
        for cell in data['cells']:
            within_bounds = (
                cell.row_number < data['number_of_rows'] and
                cell.column_number < data['number_of_columns']
            )
            if not within_bounds:
                raise ValidationError(
                    "{} is not within the bounds of the board of ({},{})".format(
                        cell, data['number_of_rows'], data['number_of_columns']))


class HitoriSolutionSchema(Schema):
    cells_on = fields.Nested(CellSchema, many=True)
    cells_off = fields.Nested(CellSchema, many=True)


def load_board(json_object_data):
    return BoardSchema(strict=True).load(json_object_data).data


def dump_solution(hitori_solution):
    return HitoriSolutionSchema(strict=True).dump(hitori_solution).data
