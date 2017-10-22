from celery import (
    chain,
    signature
)

from pyramid_celery import celery_app as app


from puzzle_app.engine_api.hitori_engine_api import (
    make_hitori_engine_data,
    read_hitori_engine_data,
    update_hitori_solve_status
)

from puzzle_app.models import HITORI_SOLVE_STATUS


@app.task
def hitori_engine_input(hitori_game_board_id, solve_id):
    data = make_hitori_engine_data(hitori_game_board_id)
    return dict(solve_id=solve_id, **data)


hitori_solve = signature('puzzle_engine.engine_worker.run_hitori_solve')


@app.task
def hitori_engine_output(hitori_engine_solution):
    return read_hitori_engine_data(hitori_engine_solution)


@app.task
def hitori_solve_status(*args, **kwargs):
    solve_id = kwargs['solve_id']
    status = kwargs['status']
    update_hitori_solve_status(solve_id, status)


def get_hitori_solve_chain(board_id, solve_id):
    return chain(
        hitori_engine_input.s(board_id, solve_id),
        hitori_solve,
        hitori_engine_output.s(),
        hitori_solve_status.s(solve_id=solve_id, status=HITORI_SOLVE_STATUS.SUCCESS.name)
    ).on_error(hitori_solve_status.s(solve_id=solve_id, status=HITORI_SOLVE_STATUS.FAILURE.name))
