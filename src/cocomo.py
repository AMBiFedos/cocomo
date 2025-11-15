from constants import *

def schedule_estimate(size: int, em_prod: float, sf_sum: float) -> float:
    E = B + 0.01 * sf_sum
    return A * size**E * em_prod

