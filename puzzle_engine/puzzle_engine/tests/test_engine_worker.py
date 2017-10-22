import mock
import pytest


from puzzle_engine.engine_worker import (
    run_hitori_solve
)


class TestRunHitoriSolve:
    @pytest.fixture
    def hitori_data(self):
        return {'some_field': ["some_data", "more_data"], 'another_field': "data"}

    @pytest.fixture
    def hitori_solution(self):
        return {'hitori_solution': ["some values", "?"]}

    @mock.patch('puzzle_engine.engine_worker.solve_hitori')
    def test_run_hitori_solve(self, solve_hitori, celery_config, celery_worker, hitori_data, hitori_solution):
        solve_hitori.return_value = hitori_solution
        result = run_hitori_solve(hitori_data)

        solve_hitori.assert_called_once_with(hitori_data)
        assert result == hitori_solution
