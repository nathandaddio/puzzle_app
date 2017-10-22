import mock
import pytest


from puzzle_app.jobs import (
    hitori_engine_input,
    hitori_engine_output,
    hitori_solve_status
)


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

    @mock.patch('puzzle_app.jobs.make_hitori_engine_data')
    def test_hitori_engine_input_task(
            self, make_hitori_engine_data, hitori_game_board_id,
            solve_id, hitori_engine_input_data, celery_worker, celery_config):
        make_hitori_engine_data.return_value = hitori_engine_input_data

        result = hitori_engine_input(hitori_game_board_id, solve_id)

        make_hitori_engine_data.assert_called_with(hitori_game_board_id)

        assert result == dict(solve_id=solve_id, **hitori_engine_input_data)


class TestHitoriEngineOutputTask:
    @pytest.fixture
    def hitori_engine_solution(self):
        return {}

    @mock.patch('puzzle_app.jobs.read_hitori_engine_data')
    def test_hitori_engine_output_task(self, read_hitori_engine_data, hitori_engine_solution):
        result = hitori_engine_output(hitori_engine_solution)

        read_hitori_engine_data.assert_called_once_with(hitori_engine_solution)

        assert result == read_hitori_engine_data.return_value


class TestHitoriSolveStatus:
    @pytest.fixture
    def solve_id(self):
        return 3

    @pytest.fixture
    def status(self):
        return "FAILURE"

    @mock.patch('puzzle_app.jobs.update_hitori_solve_status')
    def test_update_hitori_solve_status_task(self, update_hitori_solve_status, solve_id, status):
        hitori_solve_status(solve_id=solve_id, status=status)

        update_hitori_solve_status.assert_called_once_with(solve_id, status)
