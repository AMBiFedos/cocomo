from textual.app import App, ComposeResult
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal, Vertical, Grid, Container
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input, Button, Header, Footer, Select, TabbedContent, TabPane, Static, Rule, ListItem, ListView

from pathlib import Path
import json

from cocomo import Project, Module, ProjectEncoder
from constants import RatingLevel, EffortModifier

class FileItem(ListItem):

    def __init__(self, text: str) -> None:
        super().__init__()
        self.text = text

    def compose( self ) -> ComposeResult:
        yield Label(self.text)

class LoadScreen(ModalScreen[Path]):
    
    def compose(self):
        with Container():
            yield Label("Path:")
            initial_path: Path = Path(Path.home(), "cocomo-projects")
            if not initial_path.exists():
                initial_path = Path.home()
            yield Input(str(initial_path), id="load_path")
            
            yield ListView(*self.get_file_list_items(initial_path), id="file_list")
            with Horizontal():
                yield Button("OK", id="ok_button")
                yield Button("Cancel", id="cancel_button")

    def get_file_list_items(self, load_path: Path) -> list[ListItem]:
        file_list: list[str] = []
        for child in load_path.iterdir():
            if child.is_file():
                file_list.append(child.name)
        file_list.sort()

        list_items: list[ListItem] = []
        for file_name in file_list:
            list_items.append(FileItem(file_name))
        
        return list_items

    @on(Button.Pressed, "#ok_button")
    def load_file(self):
        file_name: str = self.query_one("#file_list").highlighted_child.text
        load_path: Path = Path(self.query_one("#load_path").value, file_name)
        self.dismiss(load_path)

    @on(Button.Pressed, "#cancel_button")
    def cancel_load(self):
        self.dismiss(None)
        
    @on(Input.Changed, "#load_path")
    def update_path(self):
        load_path: Path = Path(self.query_one("#load_path").value)
        while not load_path.exists():
            load_path = load_path.parent

        list_items = self.get_file_list_items(load_path)
        self.query_one("#file_list").clear()
        for item in list_items:
            self.query_one("#file_list").append(item)

class SaveScreen(ModalScreen[Path]):
    path_not_exist_msg: str = "The path does not exist and will be created."
    file_exists_msg: str = "[b][red]Warning[/red][/b]: This file already exists and will be [b]overwritten[/b]."
    
    def __init__(self, file_name: str = "project", name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.file_name: str = file_name
    
    def compose(self):
        with Container():
            yield Label("Path:")
            initial_path: Path = Path(Path.home(), "cocomo-projects")
            yield Input(str(initial_path), id="save_path")
            path_msg = "" if initial_path.exists() else self.path_not_exist_msg
            yield Label(path_msg, id="path_msg")
            yield Label("File Name:")
            file_name: str = self.file_name + ".json"
            yield Input(file_name, id="save_file")
            file_msg = "" if not Path(initial_path, file_name).exists() else self.file_exists_msg
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
            path_msg.update(self.path_not_exist_msg)
        else:
            path_msg.update("")

    @on(Input.Changed, "#save_file")
    def validate_file_name(self):
        save_path: Path = Path(self.query_one("#save_path").value, self.query_one("#save_file").value)
        file_msg: Label = self.query_one("#file_msg")
        if save_path.exists():
            file_msg.update(self.file_exists_msg)
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
        ("n", "new_project", "New Project"),
        ("o", "open_project", "Open Project"),
        ("s", "save_project", "Save Project"),
        ("r", "rename_project", "Rename Project"),
        ("a", "add_module", "Add Module"),
    ]
    
    projects_directory = "projects"
    
    def __init__(self):
        super().__init__()
        self.project: Project = Project("Untitled")
        self.project.add_module(Module("Module 1"))
        self.new_module_count: int = 1

    def on_mount(self):
        self.theme = "nord"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        

        with Grid(id="project_header"):
            yield Label("Project Name")
            yield Label("Schedule Factor")
            yield Static("")
            yield Static("")
            yield Input(self.project.name, id="project_name", disabled=True)
            yield Select([(i.value, i) for i in RatingLevel], id="sched_select", value=self.project.schedule_factor, allow_blank=False)
            yield Button("Scale Factors")
            yield Button("Report")
            
            
        with TabbedContent():
            for module in self.project.modules:
                yield ModulePane(module)

        
        self.sidebar: Static = Static("\n\nPlaceholder", id="sidebar")
        yield self.sidebar
        
    async def action_new_project(self):
        self.project = Project("Untitled")
        self.project.add_module(Module("Module 1"))
        self.new_module_count = 1
        await self.refresh_values()

    def action_open_project(self):
        self.push_screen(LoadScreen(), self.load_screen_callback)
    
    async def load_screen_callback(self, load_path: Path) -> None:
        if load_path is None:
            return

        self.sidebar.update(str(load_path))
        project_json = load_path.read_text()
        project_data = json.loads(project_json)
        self.project = Project.project_from_dict(project_data)
        self.new_module_count = 1
        
        await self.refresh_values()

    async def refresh_values(self) -> None:

        self.query_one("#project_name", Input).value = self.project.name
        self.query_one("#sched_select").value=self.project.schedule_factor

        modules: TabbedContent = self.query_one(TabbedContent)
        module_list: str = ""
        await modules.clear_panes()
        for module in self.project.modules:
            module_list += module.name + "\n"
            modules.add_pane(ModulePane(module))

        self.sub_title = self.project.name

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
        project_name = self.query_one("#project_name")
        project_name.disabled=False
        self.set_focus(project_name, True)

    def action_add_module(self):
        self.new_module_count += 1
        module: Module = Module(f"Module {self.new_module_count}")
        self.project.add_module(module)
        self.query_one(TabbedContent).add_pane(ModulePane(module))

    @on(Input.Submitted, "#project_name")
    @on(Input.Blurred, "#project_name")
    def rename_project(self):
        project_name = self.query_one("#project_name")
        project_name.disabled=True
        self.project.name = project_name.value
        self.sub_title = self.query_one("#project_name").value
        
    @on(Select.Changed, "#sched_select")
    def select_schedule_factor(self):
        self.project.schedule_factor = RatingLevel(self.query_one("#sched_select").value)


if __name__ == "__main__":
    CocomoApp().run()