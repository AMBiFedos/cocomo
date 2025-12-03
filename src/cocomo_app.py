from textual.app import App
from textual import on
from textual.screen import Screen, ModalScreen
from textual.containers import Horizontal
from textual.message import Message
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, Input, Button, Header, Footer, Rule

from pathlib import Path


from cocomo import *


# class ProjectManager(Widget):
#     DEFAULT_CSS = """
#     ProjectListing {
#         height: 2;
#     }
#     """
    
#     TITLE = "COCOMO II.2000"
#     SUB_TITLE = "Untitled"


#     class Load(Message):
#         def __init__(self, item):
#             super().__init__()
#             self.item = item
            
#     class Delete(Message):
#         def __init__(self, item):
#             super().__init__()
#             self.item = item
    
#     def __init__(self, project_name: str="Untitled"):
#         super().__init__()
#         self.project_name = Input(project_name, id="project")
        
#     def compose(self):
#         with Horizontal():
#             yield Button("Load", id="load")
#             yield Button("Rename", id="rename")
#             yield Button("Delete", id="delete")
#             yield self.project_name

class ProjectName(Widget):
    def compose(self):
        with Horizontal():
            yield Label("Project: ")
            yield Input("Untitled", id="project_name")

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
    ]
    
    projects_path = "../projects"
    
    module_item: ModuleListing = None


    def __init__(self):
        super().__init__()
        self.project: Project = Project("Untitled")
        self.module: Module = Module("My Module")
        self.project.add_module(self.module)
        self.module_item: ModuleListing = ModuleListing(self.module)

    def compose(self):
        yield Header()
        yield Footer()
        yield ProjectName()
        yield Rule(line_style="double")
        yield self.module_item
        
        
        
    @on(Input.Submitted, "#project_name")
    def update_project_name(self):
        self.sub_title = self.query_one("#project_name").value


    def load_projects(self):
        p: Path = Path(self.projects_path)
        for child in p.iterdir():
            self.projects.append(child)
            
        
        


if __name__ == "__main__":
    CocomoApp().run()