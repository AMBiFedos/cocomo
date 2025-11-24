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
        
        self.nominal_schedule += child.nominal_schedule
        
    def remove_child(self, child: Csci) -> Union[Csci, None]:
        
        for i in range(0, len(self.children)):
            if self.children[i] is child:
                self.nominal_schedule -= child.nominal_schedule
                return self.children.pop(i)      
        return None
        
class CsciChild(Csci):
    def __init__(self, title: str, parent: Union[CsciParent, None]=None):
        super().__init__(title)
        self.ksloc = 100
        self.em_prod: float = 1.0
        self.sf_sum: float = 24.0
        self.function_points: int = 0
        self.nominal_schedule = 0.0
        self.language = "C"
        
        self.parent = parent
        if parent is not None:
            parent.add_child(self)
        
    def change_parent(self, new_parent: CsciParent) -> None:
        new_parent.add_child(self)
        if self.parent is not None:
            self.parent.remove_child(self)
            self.parent = new_parent
    
    
    def estimate_schedule(self) -> float:
        E: float = B + 0.01 * self.sf_sum
        self.nominal_schedule = A * self.ksloc**E * self.em_prod
        

    def calculate_function_points(self, function_counts: dict[str, tuple[int, int, int]]) -> None:
        fp: int = 0

        for count in function_counts:
            fp += sum(tuple(count * weight for count, weight in zip(function_counts[count], WEIGHTS[count])))

        self.function_points = fp

    def function_points_to_ksloc(self) -> None:
        ratios: dict[str, int] = {}
        with open("data/ufp_to_ksloc_ratios.json") as json_file:
            ratios = json.load(json_file)
        
        self.ksloc = self.function_points * ratios[self.language]

    # def get_equivalent_ksloc(adapted_ksloc: int, at: int, ) ->