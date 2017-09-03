import pytest


from marshmallow import ValidationError


from puzzle_app.schemas.hitori import (
    HitoriGameBoardCellSchema,
    HitoriGameBoardSchema,
    HitoriSolveSchema
)


def _new_dict_without_keys(dictionary, keys):
    new_dict = dict(dictionary)
    for key in keys:
        del new_dict[key]
    return new_dict


class TestHitoriGameBoardCellSchema:
    _data = {
        'id': 1,
        'row_number': 2,
        'column_number': 3,
        'value': 5,
        'included_in_solution': True
    }

    @pytest.fixture
    def data(self):
        return self._data

    def test_schema_loads_data(self, data):
        output_data = HitoriGameBoardCellSchema(strict=True).load(data).data

        assert output_data == data

    def test_schema_dumps_data(self, data):
        output_data = HitoriGameBoardCellSchema(strict=True).dump(data).data
        assert output_data == data

    bad_data = [
        {},
        {
            'row_number': 2,
            'column_number': 3,
            'value': 5,
            'included_in_solution': True
        },
        dict(_data, id=-1),
        dict(_data, row_number=-5),
        dict(_data, column_number=-50),
        dict(_data, value=-5),
        _new_dict_without_keys(_data, ['id']),
        _new_dict_without_keys(_data, ['row_number']),
        _new_dict_without_keys(_data, ['column_number']),
        _new_dict_without_keys(_data, ['value'])
    ]

    @pytest.mark.parametrize('bad_data', bad_data)
    def test_bad_data_raises_validation_error(self, bad_data):
        with pytest.raises(ValidationError):
            HitoriGameBoardCellSchema(strict=True).load(bad_data)


class TestHitoriGameBoardSchema:
