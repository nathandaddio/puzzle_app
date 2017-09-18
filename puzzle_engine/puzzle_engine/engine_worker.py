from celery import Celery


from puzzle_engine.hitori.solve import solve_hitori


app = Celery()


@app.task(queue='engine_worker')
def run_hitori_solve(hitori_data):
    try:
        return solve_hitori(hitori_data)
    except:
        return {'feasible': False, 'cells_on': [], 'cells_off': [], 'board': hitori_data['id']}
