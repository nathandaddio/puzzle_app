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


@app.task
def hitori_engine_input(hitori_game_board_id):
    return make_hitori_engine_data(hitori_game_board_id)


hitori_solve = signature('puzzle_engine.engine_worker.run_hitori_solve')


@app.task
def hitori_engine_output(hitori_engine_solution):
    return read_hitori_engine_data(hitori_engine_solution)


@app.task
def hitori_solve_status(hitori_engine_output_result, solve_id):
    update_hitori_solve_status(solve_id)


def get_hitori_solve_chain(board_id, solve_id):
    return chain(
        hitori_engine_input.s(board_id),
        hitori_solve,
        hitori_engine_output.s(),
        hitori_solve_status.s(solve_id)
    )
