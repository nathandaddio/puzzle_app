CELERY_IMPORTS = (
    'puzzle_engine.engine_worker'
)


CELERY_ROUTES = {
    "puzzle_engine.engine_worker.run_hitori_solve": {
        "queue": "engine_worker",
        "exchange": "engine_worker",
        "routing_key": "engine_worker"
    },
    "puzzle_app.jobs.hitori_engine_output": {
        "queue": "puzzle_app",
    },
    "puzzle_app.jobs.hitori_engine_input": {
        "queue": "puzzle_app",
    }
}

CELERY_RESULT_BACKEND = 'rpc'

BROKER_URL = 'amqp://guest:guest@localhost:5673/puzzle_app'
