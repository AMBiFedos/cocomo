from textual.app import App, ComposeResult
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal, Vertical, Grid
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input, Button, Header, Footer, Select, TabbedContent, TabPane, Static

from pathlib import Path

from cocomo import Project, Module
from constants import RatingLevel, EffortModifier

    
# class ModulePane(Widget):
    
    
    
#     def __init__(self, module: Module):
#         super().__init__()
#         self.module: Module = module
        
    
#     def compose(self):
#         pass    

class CocomoApp(App):
    CSS_PATH = "cocomo.css"
    TITLE = "COCOMO II.2000"    
    SUB_TITLE = "Untitled"
    
    BINDINGS = [
        ("n", "new_project"),
        ("o", "open_project"),
        ("r", "rename_project", "Rename Project"),
        # ("a", "add_module", "Add Module"),
    ]
    
    projects_path = "../projects"
    
    # module_item: ModulePane = None


    def __init__(self):
        super().__init__()
        self.project: Project = Project("Untitled")
        self.project.add_module(Module("Module 1"))

    def on_mount(self):
        self.theme = "catppuccin-latte"
        

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Vertical(id="main_area"):
            # yield ProjectHeader(self.project)
            with Grid(id="project_header"):
                yield Label("Project Name")
                yield Label("Schedule Factor")
                yield Static("")
                yield Static("")
                yield Input(self.project.name, id="project_name", disabled=True)
                yield Select([(i.value, i.name) for i in RatingLevel], id="sched_select", value=self.project.SCED.name, allow_blank=False)
                yield Button("Scale Factors")
                yield Button("Report")
            
            
            with TabbedContent():
                for module in self.project.modules:
                    with TabPane(module.name, id=module.name.lower().replace(" ", "")):
                        with Horizontal(id="sloc"):
                            yield Label("Lines of Code:")
                            yield Input(str(module.sloc))
                        with Grid(classes="effort_modifiers"):
                            for key, value in module.effort_modifiers.items():
                                with Vertical():
                                    yield Label(key.name)
                                    yield Select([(i.value, i.name) for i in RatingLevel], id="sched_select", value=value.name, allow_blank=False)
        
        yield Static("\n\nPlaceholder", id="sidebar")
        
    @on(Input.Submitted, "#project_name")
    def update_project_name(self):
        self.sub_title = self.query_one("#project_name").value


    def load_projects(self):
        p: Path = Path(self.projects_path)
        for child in p.iterdir():
            self.projects.append(child)
            
            
if __name__ == "__main__":
    CocomoApp().run()