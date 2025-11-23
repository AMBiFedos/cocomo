from typing import Union
import json
from constants import *

class Csci:
    def __init__(self, title: str):
        self.title = title
        

class CsciParent(Csci):
    def __init__(self, title: str, children: list[Csci]=[]):
        super().__init__(title)
        self.children: list[Csci] = children
        self.nominal_schedule: float = 0.0

    def add_child(self, child:Csci) -> None:
        if child not in self.children:
            self.children.append(child)
        
    def remove_child(self, child: Csci) -> Union[Csci, None]:
        
        for i in range(0, len(self.children)):
            if self.children[i] is child:
                return self.children.pop(i)      
        return None
    
    
    def update_schedule_estimate(self, child_estimate: float):
        self.nominal_schedule += child_estimate
        
class CsciChild(Csci):
    def __init__(self, title: str, parent: Union[CsciParent, None]=None):
        super().__init__(title)
        self.size = 100
        self.em_prod: float = 1.0
        self.sf_sum: float = 24.0
        self.function_points: int = 0
        self.nominal_schedule = 0.0
        
        self.parent = parent
        parent.add_child(self)
        
    def estimate_schedule(self) -> float:
        E: float = B + 0.01 * self.sf_sum
        self.nominal_schedule = A * self.ksloc**E * self.em_prod
        

    def calculate_ufp(self, function_point_counts: dict[str, tuple[int, int, int]]) -> None:
        fp: int = 0

        for function_point in function_point_counts:
            fp += sum(tuple(count * weight for count, weight in zip(function_point_counts[function_point], WEIGHTS[function_point])))

        self.function_points = fp

    def ufp_to_ksloc(self, ufp: int, language: str) -> int:
        ratios = {}
        with open("data/ufp_to_sloc_ratios.json") as json_file:
            ratios = json.load(json_file)
        
        self.ksloc = ufp * ratios[language]
        return self.ksloc

    # def get_equivalent_ksloc(adapted_ksloc: int, at: int, ) ->