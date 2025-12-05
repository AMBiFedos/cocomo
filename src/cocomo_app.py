from textual.app import App, ComposeResult
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal, Vertical
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input, Button, Header, Footer, Tree, TabbedContent, TabPane, Static

from pathlib import Path


from cocomo import *

class ProjectHeader(Widget):
    
    project : Project
    project_name: str = reactive("")
    
    def __init__(self, project: Project):
        super().__init__()
        self.project: Project = project
        self.project_name = project.name
        
        self.project_name_input: Input = Input(self.project_name, id="project_name")
        
    
    def compose(self) -> ComposeResult:
        with Horizontal():
            yield self.project_name_input
            yield Button("Schedule")
            yield Button("Scale Factors")
            yield Button("Report")
            
    def watch_project_name(self, project_name) -> None:
        self.project.name = project_name
    
    @on(Input.Submitted, "#project_name")
    def update_project_name(self)-> None:
        self.project_name = self.query_one("#project_name").value

class ModuleListing(Widget):
    
    description = reactive("")
    
    class Edit(Message):
        def __init__(self, item):
            super().__init__()
            self.item = item
    
    class Delete(Message):
        def __init__(self, item):
            super().__init__()
            self.item = item
    
    def __init__(self, module: Module):
        super().__init__()
        self.module: Module = module
        self.description_label: Label = Label(id="description")
        
        self.description = f"{self.module.name} | {self.module.sloc/1000} ksloc"
    
    def compose(self):
        with Horizontal():
            yield Button("Edit", id="edit")
            yield Button("Delete", id="delete")
            yield self.description_label
    
    def watch_description(self, description):
        self.description_label.update(description)
    
    
    @on(Button.Pressed, "#edit")
    def edit_request(self):
        self.post_message(self.Edit(self))
        
    @on(Button.Pressed, "#delete")
    def delete_request(self):
        self.post_message(self.Delete(self))

    

class CocomoApp(App):
    CSS_PATH = "cocomo.css"
    TITLE = "COCOMO II.2000"    
    SUB_TITLE = "Untitled"
    
    BINDINGS = [
        ("n", "new_project", "New Project"),
        ("o", "open_project", "Open Project"),
        # ("a", "add_module", "Add Module")
    ]
    
    projects_path = "../projects"
    
    module_item: ModuleListing = None


    def __init__(self):
        super().__init__()
        self.project: Project = Project("Untitled")
        self.project.add_module(Module("Module 1"))


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        
        with Horizontal():
            with Vertical(id="main_area"):
                yield ProjectHeader(self.project)
                with TabbedContent(initial="module1"):
                    with TabPane("Module 1", id="module1"):
                        yield Static("Module 1")
            
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