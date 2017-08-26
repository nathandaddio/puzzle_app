from puzzle_engine.hitori.engine import hitori_solve
from puzzle_engine.hitori.schemas import (
    load_board,
    dump_solution
)
from puzzle_engine.hitori.models import EngineData


def solve(json_obj_data):
    board = load_board(json_obj_data)
    engine_data = EngineData(board)
    solution = hitori_solve(engine_data)
    return dump_solution(solution)
