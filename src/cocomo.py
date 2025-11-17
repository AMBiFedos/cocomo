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
        
    def remove_child(self, child: Csci) -> Csci:
        for i in range(0, len(self.children)):
            if self.children[i] is child:
                return self.children.pop(i)      
        return None
    
    def update_schedule_estimate(self, child_estimate: float):
        self.nominal_schedule += child_estimate
        
        

class CsciChild(Csci):
    def __init__(self, title, str, parent: CsciParent=None):
        super().__init__(title)
        self.parent = parent        
        
    def estimate_schedule(self, ksloc: int, em_prod: float, sf_sum: float) -> float:
        E: float = B + 0.01 * sf_sum
        self.nominal_schedule = A * ksloc**E * em_prod
        return self.nominal_schedule

    def calculate_ufp(self, function_point_counts: dict[str, tuple[int, int, int]]) -> int:
        total_fp:int = 0

        for function_point in function_point_counts:
            total_fp += sum(tuple(count * weight for count, weight in zip(function_point_counts[function_point], WEIGHTS[function_point])))

        return total_fp

    def ufp_to_ksloc(self, ufp: int, language: str) -> int:
        ratios = {}
        with open("data/ufp_to_sloc_ratios.json") as json_file:
            ratios = json.load(json_file)
        
        self.ksloc = ufp * ratios[language]
        return self.ksloc

    # def get_equivalent_ksloc(adapted_ksloc: int, at: int, ) ->