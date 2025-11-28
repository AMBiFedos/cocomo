from typing import Union
import json
import math

from constants import *

class Module:
    def __init__(self, name: str):
        self.name: str = name
        self.ksloc: int = 0
        self.effort_modifiers: dict[EffortModifier, RatingLevel] = {
            EffortModifier.RELY: RatingLevel.NOMINAL,
            EffortModifier.DATA: RatingLevel.NOMINAL,
            EffortModifier.CPLX: RatingLevel.NOMINAL,
            EffortModifier.RUSE: RatingLevel.NOMINAL,
            EffortModifier.DOCU: RatingLevel.NOMINAL,
            EffortModifier.TIME: RatingLevel.NOMINAL,
            EffortModifier.STOR: RatingLevel.NOMINAL,
            EffortModifier.PVOL: RatingLevel.NOMINAL,
            EffortModifier.ACAP: RatingLevel.NOMINAL,
            EffortModifier.PCAP: RatingLevel.NOMINAL,
            EffortModifier.PCON: RatingLevel.NOMINAL,
            EffortModifier.APEX: RatingLevel.NOMINAL,
            EffortModifier.PLEX: RatingLevel.NOMINAL,
            EffortModifier.LTEX: RatingLevel.NOMINAL,
            EffortModifier.TOOL: RatingLevel.NOMINAL,
            EffortModifier.SITE: RatingLevel.NOMINAL,
            EffortModifier.SCED: RatingLevel.NOMINAL,
        }
        self.em_prod: float = 1.0
        self.function_points: int = 0
        self.language: Language = Language.C
        self.nominal_schedule: float = 0.0

    def estimate_schedule(self, scale_factor_sum: int):
        em_values = list(self.effort_modifiers.values())
        # Need to create dictionary for EM and SF tables then lookup using RatingLevel
        
        E: float = B + 0.01 * scale_factor_sum
        self.nominal_schedule = A * self.ksloc**E * effort_mod_prod

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

        self.scale_factors: dict[ScaleFactor, RatingLevel] = {
            ScaleFactor.PREC: RatingLevel.NOMINAL,
            ScaleFactor.FLEX: RatingLevel.NOMINAL,
            ScaleFactor.RESL: RatingLevel.NOMINAL,
            ScaleFactor.TEAM: RatingLevel.NOMINAL,
            ScaleFactor.PMAT: RatingLevel.NOMINAL,
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

