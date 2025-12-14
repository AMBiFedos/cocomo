from typing import Union
import json
import math

from constants import *

class Module:
    def __init__(self, name: str):
        self.name: str = name
        self.project: Project = None
        self.sloc: int = 0
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
        }
        self.em_prod: float = 1.0
        self.function_points: int = 0
        self.language: Language = Language.C
        self.nominal_effort: float = 0.0
        self.nominal_schedule: float = 0.0

    def estimate_effort(self):
        effort_modifier_prod: float = 1.0
        for key, value in self.effort_modifiers.items():
            effort_modifier_prod *= EFFORT_MODIFIER_COST_DRIVERS[key][value]
        effort_modifier_prod *= SCHEDULE_COST_DRIVER[self.project.schedule_factor]
        
        scale_factor_sum = 0
        for key, value in self.project.scale_factors.items():
            scale_factor_sum += SCALE_FACTOR_VALUES[key][value]
        
        E: float = B + 0.01 * scale_factor_sum
        self.nominal_effort = A * (self.sloc / 1000.0)**E * effort_modifier_prod

    def calculate_function_points(self, function_counts: dict[str, tuple[int, int, int]]) -> None:
        fp: int = 0

        for count in function_counts:
            fp += sum(tuple(count * weight for count, weight in zip(function_counts[count], FUNCTION_POINT_WEIGHTS[count])))

        self.function_points = fp

    def function_points_to_sloc(self) -> None:
        self.sloc = self.function_points * FUNCTION_POINT_LANGUAGE_RATIOS[self.language]

    def encode(self):
        return ModuleEncoder().default(self)

    def module_from_dict(data: dict) -> 'Module':
        module = Module(data["name"])
        module.sloc = data["sloc"]
        module.effort_modifiers = {EffortModifier[key]: RatingLevel[value] for key, value in data["effort_modifiers"].items()}
        module.function_points = data["function_points"]
        module.language = Language[data["language"]]
        return module

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

        self.schedule_factor = RatingLevel.NOMINAL
        self.modules: list[Module] = []
        self.nominal_effort: float = 0.0

    def add_module(self, module: Module, position: int=-1) -> None:
        if module not in self.modules:
            module.project = self
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

    def estimate_effort(self):
        aggregate_sloc: int = 0
        for module in self.modules:
            aggregate_sloc += module.sloc
        
        scale_factor_sum = 0
        for key, value in self.scale_factors.items():
            scale_factor_sum += SCALE_FACTOR_VALUES[key][value]
        E: float = B + 0.01 * scale_factor_sum
        
        basic_effort: float = A * (aggregate_sloc / 1000)**E * SCHEDULE_COST_DRIVER[self.schedule_factor]
        
        aggregate_basic_effort: float = 0.0
        for module in self.modules:
            basic_effort_i: float = basic_effort * (module.sloc / aggregate_sloc)
            
            effort_modifier_prod: float = 1.0
            for key, value in module.effort_modifiers.items():
                effort_modifier_prod *= EFFORT_MODIFIER_COST_DRIVERS[key][value]
            effort_modifier_prod *= SCHEDULE_COST_DRIVER[self.schedule_factor]
                
            aggregate_basic_effort += basic_effort_i * effort_modifier_prod

        self.nominal_effort = aggregate_basic_effort

    def encode(self):
        return ProjectEncoder().default(self)
    
    def project_from_dict(data: dict) -> 'Project':
        project = Project(data["name"])
        project.scale_factors = {ScaleFactor[key]: RatingLevel[value] for key, value in data["scale_factors"].items()}
        project.schedule_factor = RatingLevel[data["schedule factor"]]
        for module_data in data["modules"]:
            module = Module.module_from_dict(module_data)
            project.add_module(module)
        return project

class ModuleEncoder(json.JSONEncoder):
    def default(self, obj: Module) -> dict[str, Union[str, int, dict]]:
        if isinstance(obj, Module):
            return {
                "name": obj.name,
                "sloc": obj.sloc,
                "effort_modifiers": {key.name: value.name for key, value in obj.effort_modifiers.items()},
                "function_points": obj.function_points,
                "language": obj.language.name,
            }
        return super().default(obj)

class ProjectEncoder(json.JSONEncoder):
    def default(self, obj: Project) -> dict[str, Union[str, dict, list]]:
        if isinstance(obj, Project):
            return {
                "name": obj.name,
                "scale_factors": {key.name: value.name for key, value in obj.scale_factors.items()},
                "schedule factor": obj.schedule_factor.name,
                "modules": [module.encode() for module in obj.modules],
            }
        return super().default(obj)