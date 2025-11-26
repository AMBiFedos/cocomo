from typing import Union
import json
from constants import *

class Module:
    def __init__(self, name: str):
        self.name = name
        self.ksloc = 0
        self.em_prod: float = 1.0
        self.function_points: int = 0
        self.language = "C"
        self.nominal_schedule = 0

    def estimate_schedule(self, scale_factor: int):
        E: float = B + 0.01 * scale_factor
        self.nominal_schedule = A * self.ksloc**E * self.em_prod

    def calculate_function_points(self, function_counts: dict[str, tuple[int, int, int]]) -> None:
        fp: int = 0

        for count in function_counts:
            fp += sum(tuple(count * weight for count, weight in zip(function_counts[count], FUNCTION_POINT_WEIGHTS[count])))

        self.function_points = fp

    def function_points_to_ksloc(self) -> None:
        self.ksloc = self.function_points * FUNCTION_POINT_LANGUAGE_RATIOS[self.language]

class Project:
    def __init__(self, name: str):
        self.name = name

        self.scale_factors: dict[str, str] = {
            "PREC": RatingLevel.NOMINAL,
            "FLEX": RatingLevel.NOMINAL,
            "RESL": RatingLevel.NOMINAL,
            "TEAM": RatingLevel.NOMINAL,
            "PMAT": RatingLevel.NOMINAL,
            }

        self.modules: list[Module] = []

    def add_module(self, module: Module, position: int=-1) -> None:
        if module not in self.modules:
            if position < 0:
                self.modules.append(module)
            else:
                self.modules.insert(position, module)

    def remove_module(self, position: int) -> None:
        self.modules.pop(position)
    
    def move_module(self, old_position: int, new_position: int=-1) -> None:
        if old_position > len(self.modules) or new_position > len(self.modules):
            raise Exception("position out of bounds")

        module: Module = self.modules.pop(old_position)
        self.modules.insert(new_position, module)

