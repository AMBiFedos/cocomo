from textual.app import ComposeResult
from textual import on
from textual.screen import ModalScreen
from textual.containers import Horizontal, Vertical, Grid, Container
from textual.widgets import Label, Input, Button, Select, TabPane, Rule, ListItem, ListView, Markdown

from pathlib import Path

from cocomo import Module
from constants import RatingLevel, EffortModifier, ScaleFactor


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

class ScaleFactorScreen(ModalScreen[str]):
    def __init__(self, scale_factors: dict[ScaleFactor, RatingLevel], name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.scale_factors: dict = scale_factors

    def compose(self):
        with Container():
            for key, value in self.scale_factors.items():
                with Horizontal():
                    yield Label(key.name)
                    yield Select([(i.value, i) for i in RatingLevel], value=value, 
                                    allow_blank=False, id=key.name)
            with Horizontal():
                yield Button("OK", id="ok_button")
                yield Button("Cancel", id="cancel_button")

    @on(Button.Pressed, "#ok_button")
    def set_scale_factors(self):
        for key in self.scale_factors.keys():
            self.scale_factors[key] = self.query_one(f"#{key.name}").value
        self.dismiss("ok")

    @on(Button.Pressed, "#cancel_button")
    def cancel_scale_factors(self):
        self.dismiss(None)

class ModuleRenameScreen(ModalScreen[str]):
    def __init__(self, module_name: str, name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.module_name: str = module_name

    def compose(self):
        yield Label("Module Name:")
        yield Input(self.module_name, id="module_name_input")
        with Horizontal():
            yield Button("OK", id="ok_button")
            yield Button("Cancel", id="cancel_button")

    @on(Button.Pressed, "#ok_button")
    def rename_module(self):
        module_name: str = self.query_one("#module_name_input").value
        self.dismiss(module_name)

    @on(Button.Pressed, "#cancel_button")
    def cancel_rename(self):
        self.dismiss(None)

class ModulePane(TabPane):
    
    def __init__(self, module: Module, *children, name = None, disabled = False):
        id = module.name.lower().replace(" ", "") + "_tab"
        super().__init__(module.name, *children, name=name, id=id, classes="module_tabs", disabled=disabled)
        self.module: Module = module

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
    
    @on(Input.Blurred, "#sloc_input")
    @on(Input.Submitted, "#sloc_input")
    def update_module_sloc(self, event: Input.Changed):
        try:
            new_sloc: int = int(event._sender.value)
            if new_sloc < 0:
                raise ValueError("SLOC cannot be negative")
            self.module.sloc = new_sloc
        except ValueError:
            event._sender.value = str(self.module.sloc)