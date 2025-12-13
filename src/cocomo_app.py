from textual.app import App, ComposeResult
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal, Vertical, Grid, Container, Center
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input, Button, Header, Footer, Select, TabbedContent, TabPane, Static, Rule

from pathlib import Path
import json

from cocomo import Project, Module, ProjectEncoder
from constants import RatingLevel, EffortModifier


class SaveScreen(ModalScreen[Path]):
    def __init__(self, file_name: str = "project", name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.file_name: str = file_name
    
    def compose(self):
        with Container():
            yield Label("Path:")
            initial_path: Path = Path(Path.home(), "cocomo-projects")
            yield Input(str(initial_path), id="save_path")
            path_msg = "" if initial_path.exists() else "The path does not exist and will be created."
            yield Label(path_msg, id="path_msg")
            yield Label("File Name:")
            file_name: str = self.file_name + ".json"
            yield Input(file_name, id="save_file")
            file_msg = "" if not Path(initial_path, file_name).exists() else "Warning: This file already exists and will be overwritten."
            yield Label(file_msg, id="file_msg")
            with Horizontal():
                yield Button("OK", id="ok_button")
                yield Button("Cancel", id="cancel_button")

    @on(Button.Pressed, "#ok_button")
    def save_file(self):
        save_path: Path = Path(self.query_one("#save_path").value, self.query_one("#save_file").value)
        self.dismiss(save_path)
    
    @on(Button.Pressed, "#cancel_button")
    def cancel_save(self):
        self.dismiss(None)
        
    @on(Input.Changed, "#save_path")
    def validate_path(self):
        save_path: Path = Path(self.query_one("#save_path").value)
        path_msg: Label = self.query_one("#path_msg")
        if not save_path.exists():
            path_msg.update("The path does not exist and will be created.")
        else:
            path_msg.update("")

    @on(Input.Changed, "#save_file")
    def validate_file_name(self):
        save_path: Path = Path(self.query_one("#save_path").value, self.query_one("#save_file").value)
        file_msg: Label = self.query_one("#file_msg")
        if save_path.exists():
            file_msg.update("Warning: This file already exists and will be overwritten.")
        else:
            file_msg.update("")


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
                                    allow_blank=False, id=key.name)

    @on(Select.Changed)
    def update_effort_modifier(self, event: Select.Changed):
        self.module.effort_modifiers[EffortModifier[event._sender.id]] = event._sender.value

class CocomoApp(App):
    CSS_PATH = "cocomo.tcss"
    TITLE = "COCOMO II.2000"    
    SUB_TITLE = "Untitled"
    
    BINDINGS = [
        ("n", "new_project"),
        ("o", "open_project"),
        ("s", "save_project", "Save Project"),
        ("r", "rename_project", "Rename Project"),
        ("a", "add_module", "Add Module"),
    ]
    
    projects_directory = "projects"
    
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
                yield Select([(i.value, i) for i in RatingLevel], id="sched_select", value=self.project.schedule_factor, allow_blank=False)
                yield Button("Scale Factors")
                yield Button("Report")
            
            
            with TabbedContent():
                for module in self.project.modules:
                    yield ModulePane(module)
        
        self.sidebar: Static = Static("\n\nPlaceholder", id="sidebar")
        yield self.sidebar
        
    def action_open_project(self):
        projects_path = Path(Path.cwd(),self.projects_directory)
        project_file = Path(projects_path, "project.json")
        
        if project_file.exists():
            project_json = project_file.read_text()
            project_dict = json.loads(project_json)
            self.project = Project.decode(project_dict)
            self.sidebar.update(self.project.name)
            self.sub_title = self.project.name
            
            # tabbed_content = self.query_one(TabbedContent)
            # tabbed_content.clear()
            # for module in self.project.modules:
            #     tabbed_content.add_pane(ModulePane(module))
    
    
    def action_save_project(self):
        project_name = self.project.name.replace(" ", "-")
        self.push_screen(SaveScreen(project_name), self.save_screen_callback)

    def save_screen_callback(self, save_path: Path) -> None:
        if save_path is None:
            return

        save_path.parent.mkdir(parents=True, exist_ok=True)

        project_json = json.dumps(
            self.project.encode(),
            sort_keys=False,
            indent=4,
        )
        
        save_path.write_text(
            project_json
        )

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
        self.project.schedule_factor = RatingLevel(self.query_one("#sched_select").value)



if __name__ == "__main__":
    CocomoApp().run()