from constants import *

def schedule_estimate(size: int, em_prod: float, sf_sum: float) -> float:
    E: float = B + 0.01 * sf_sum
    return A * size**E * em_prod

def calculate_ufp(function_point_counts: dict[str, tuple[int, int, int]]):
    total_fp:int = 0

    for function_point in function_point_counts:
        total_fp += sum(tuple(count * weight for count, weight in zip(function_point_counts[function_point], WEIGHTS[function_point])))

    return total_fp