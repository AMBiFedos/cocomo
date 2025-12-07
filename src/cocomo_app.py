from textual.app import App, ComposeResult
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal, Vertical, Grid
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input, Button, Header, Footer, Select, TabbedContent, TabPane, Static, Rule

from pathlib import Path

from cocomo import Project, Module
from constants import RatingLevel, EffortModifier

class ModulePane(TabPane):
    
    def __init__(self, module, *children, name = None, disabled = False):
        id = module.name.lower().replace(" ", "") + "_tab"
        super().__init__(module.name, *children, name=name, id=id, classes="module_tabs", disabled=disabled)
        self.module = module
        

    def compose(self):
        with Horizontal(id="sloc_group"):
            yield Label("Lines of Code:")
            yield Input(str(self.module.sloc), id="sloc_input")
        
        yield Rule()
                    
        with Grid(classes="effort_modifiers"):
            for key, value in self.module.effort_modifiers.items():
                with Vertical():
                    yield Label(key.name)
                    yield Select([(i.value, i) for i in RatingLevel], value=value, 
                                    allow_blank=False, id=key.name + "_select")



class CocomoApp(App):
    CSS_PATH = "cocomo.tcss"
    TITLE = "COCOMO II.2000"    
    SUB_TITLE = "Untitled"
    
    BINDINGS = [
        ("n", "new_project"),
        ("o", "open_project"),
        ("r", "rename_project", "Rename Project"),
        ("a", "add_module", "Add Module"),
    ]
    
    projects_path = "../projects"
    
    # module_item: ModulePane = None


    def __init__(self):
        super().__init__()
        self.project: Project = Project("Untitled")
        self.project.add_module(Module("Module 1"))
        self.new_module_count: int = 1

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
                self.project_name_input: Input = Input(self.project.name, id="project_name", disabled=True)
                yield self.project_name_input
                yield Select([(i.value, i) for i in RatingLevel], id="sched_select", value=self.project.SCED, allow_blank=False)
                yield Button("Scale Factors")
                yield Button("Report")
            
            
            with TabbedContent():
                for module in self.project.modules:
                    yield ModulePane(module)
        
        self.sidebar: Static = Static("\n\nPlaceholder", id="sidebar")
        yield self.sidebar
        

    def action_rename_project(self):
        self.project_name_input.disabled=False
        self.set_focus(self.project_name_input, True)
    
    
    def action_add_module(self):
        self.new_module_count += 1
        module: Module = Module(f"Module {self.new_module_count}")
        self.project.add_module(module)
        self.query_one(TabbedContent).add_pane(ModulePane(module))

    
    
    @on(Input.Submitted, "#project_name")
    @on(Input.Blurred, "#project_name")
    def rename_project(self):
        self.project_name_input.disabled=True
        self.project.name = self.project_name_input.value
        self.sidebar.update(self.project.name)
        self.sub_title = self.query_one("#project_name").value
        
    @on(Select.Changed, "#sched_select")
    def select_schedule_factor(self):
        self.project.SCED = RatingLevel(self.query_one("#sched_select").value)



if __name__ == "__main__":
    CocomoApp().run()