from textual.app import App, ComposeResult
from textual import on
from textual.containers import Grid
from textual.widgets import Label, Input, Button, Header, Footer, Select, TabbedContent, Markdown, Static

from pathlib import Path
import json

from cocomo import Project, Module
from cocomo_tui_elements import *
from constants import RatingLevel, EffortModifier, ScaleFactor



class CocomoApp(App):
    CSS_PATH = "cocomo.tcss"
    TITLE = "COCOMO II.2000"    
    SUB_TITLE = "Untitled"
    
    BINDINGS = [
        ("n", "new_project", "New Project"),
        ("o", "open_project", "Open Project"),
        ("s", "save_project", "Save Project"),
        ("a", "add_module", "Add Module"),
        ("r", "rename_module", "Rename Module"),
    ]
    
    projects_directory = "projects"
    
    def __init__(self):
        super().__init__()
        self.project: Project = Project("Untitled")
        self.project.add_module(Module("Module 1"))
        self.project.modules[0].sloc = 1000
        self.new_module_count: int = 1
        self.summary_str: str = ""
        # self.build_results()

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
            yield Input(self.project.name, id="project_name")
            yield Select([(i.value, i) for i in RatingLevel], id="sched_select", value=self.project.schedule_factor, allow_blank=False)
            yield Button("Scale Factors", id="scale_factors_button")
            yield Button("Report")
            
            
        with TabbedContent():
            for module in self.project.modules:
                yield ModulePane(module)

        yield Markdown(self.summary_str, id="sidebar")
        self.build_results()

    async def action_new_project(self):
        self.project = Project("Untitled")
        self.project.add_module(Module("Module 1"))
        self.project.modules[0].sloc = 1000
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
        await modules.clear_panes()
        for module in self.project.modules:
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
        module.sloc = 1000
        self.new_module_count += 1
        self.project.add_module(module)
        self.query_one(TabbedContent).add_pane(ModulePane(module))

    def action_rename_module(self):
        modules: TabbedContent = self.query_one(TabbedContent)
        current_pane: ModulePane = modules.active_pane
        self.push_screen(ModuleRenameScreen(current_pane.module.name), self.rename_module_callback)
        
    async def rename_module_callback(self, new_name: str) -> None:
        if new_name is None:
            return
        modules: TabbedContent = self.query_one(TabbedContent)
        current_pane: ModulePane = modules.active_pane
        
        old_name: str = current_pane.module.name
        current_pane.module.name = new_name
        
        for module in self.project.modules:
            if module.name == old_name:
                module.name = new_name
                break
        
        await modules.clear_panes()
        for module in self.project.modules:
            modules.add_pane(ModulePane(module))

    def build_results(self) -> None:
        self.project.estimate_effort()
        results_heading = f"# {self.project.name} - Effort Estimate"
        summary_table = """
## Estimate Summary
|     Module    |  SLOC  | Effort |
|:-------------:|:------:|:------:|
"""
        for module in self.project.modules:
            module.estimate_effort()
            summary_table += f"| {module.name} | {module.sloc} | {module.nominal_effort:.2f} |\n"

        summary_table += f"| Project Total |  | **{self.project.nominal_effort:.2f}** |\n"

        self.summary_str = f"{results_heading}\n{summary_table}"
        self.query_one("#sidebar").update(self.summary_str)

    @on(Input.Submitted, "#project_name")
    @on(Input.Blurred, "#project_name")
    def rename_project(self):
        self.project.name = self.query_one("#project_name")
        self.sub_title = self.query_one("#project_name").value
        
    @on(Select.Changed, "#sched_select")
    def select_schedule_factor(self):
        self.project.schedule_factor = RatingLevel(self.query_one("#sched_select").value)
    
    @on(Button.Pressed, "#scale_factors_button")
    def edit_scale_factors(self):
        self.push_screen(ScaleFactorScreen(self.project.scale_factors))

if __name__ == "__main__":
    CocomoApp().run()