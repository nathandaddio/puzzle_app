from marshmallow import ValidationError

from puzzle_engine.hitori.engine import (
    hitori_solve,
    HitoriSolution
)
from puzzle_engine.hitori.schemas import (
    load_board,
    dump_solution
)
from puzzle_engine.hitori.models import EngineData


def solve_hitori(json_obj_data):
    try:
        board = load_board(json_obj_data)
    except ValidationError:
        solution = HitoriSolution.infeasible_solution(board)
        return dump_solution(solution)
    engine_data = EngineData(board)
    solution = hitori_solve(engine_data)
    return dump_solution(solution)
