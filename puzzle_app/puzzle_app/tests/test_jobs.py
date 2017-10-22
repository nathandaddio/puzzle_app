import mock
import pytest


from puzzle_app.jobs import hitori_engine_input


class TestHitoriEngineInputTask:
    @pytest.fixture
    def hitori_game_board_id(self):
        return 3

    @pytest.fixture
    def solve_id(self):
        return 593

    @pytest.fixture
    def hitori_engine_input_data(self):
        return {'blah': ["blah", "blah blah"]}

    @mock.patch('puzzle_app.jobs.make_hitori_engine_data', new_callable=mock.Mock)
    def test_hitori_engine_input_task(
            self, make_hitori_engine_data, hitori_game_board_id,
            solve_id, hitori_engine_input_data, celery_worker, celery_config):
        make_hitori_engine_data.return_value == hitori_engine_input_data

        assert make_hitori_engine_data() == hitori_engine_input_data
        result = hitori_engine_input(hitori_game_board_id, solve_id)

        make_hitori_engine_data.assert_called_with(hitori_game_board_id)
        assert result == dict(solve_id=solve_id, **hitori_engine_input_data)
