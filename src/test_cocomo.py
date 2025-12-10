import unittest
from cocomo import *
import json

class TestCocomoProject(unittest.TestCase):
    
    def test_add_module_no_position(self):
        module: Module = Module("<--test module-->")
        project: Project = Project("<--test project-->")
        project.add_module(module)
        self.assertListEqual([module], project.modules)
    
    def test_add_module_specific_position(self):
        module1: Module = Module("module 1")
        module2: Module = Module("module 2")
        project: Project = Project("project")
        
        project.add_module(module1)
        project.add_module(module2, 0)
        
        self.assertListEqual([module2, module1], project.modules)

    def test_remove_module(self):
        module1: Module = Module("module 1")
        module2: Module = Module("module 2")
        project: Project = Project("project")
        
        project.add_module(module1)
        project.add_module(module2)

        self.assertListEqual([module1, module2], project.modules)
        
        project.remove_module(0)

        self.assertListEqual([module2], project.modules)

    def test_move_module(self):
        module1: Module = Module("module 1")
        module2: Module = Module("module 2")
        project: Project = Project("project")
        
        project.add_module(module1)
        project.add_module(module2)

        self.assertListEqual([module1, module2], project.modules)

        project.move_module(1, 0)

        self.assertListEqual([module2, module1], project.modules)
        
    def test_estimate_effort(self):
        project: Project = Project("project")
        module1: Module = Module("module1")
        module1.sloc = 100000
        
        module2: Module = Module("module2")
        module2.sloc = 100000
        
        project.add_module(module1)
        project.add_module(module2)
        
        project.estimate_effort()
        
        self.assertAlmostEqual(997.2, project.nominal_effort, places=1)

    def test_project_encoder(self):
        project: Project = Project("Project 1")
        project.add_module(Module("Module 1"))
        project.add_module(Module("Module 2"))
        encoded = ProjectEncoder().default(project)
        with open('test_project.json', 'w') as file:
            json.dump(json.dumps(encoded,
                                 sort_keys=False,
                                 indent=4,
                                 ),
                      file)


class TestCocomoModule(unittest.TestCase):
    
    def test_estimate_effort_nominal(self):
        project: Project = Project("test project")
        
        module: Module = Module("test module")
        project.add_module(module)
        module.sloc = 100000
        
        module.estimate_effort()
        self.assertAlmostEqual(465.3, module.nominal_effort, places=1)

    def test_estimate_effort(self):
        project: Project = Project("test project")

        module: Module = Module("test module")
        project.add_module(module)
        module.sloc = 100000
        module.effort_modifiers[EffortModifier.ACAP] = RatingLevel.HIGH
        module.effort_modifiers[EffortModifier.PCAP] = RatingLevel.HIGH
        
        module.estimate_effort()
        self.assertAlmostEqual(348.1, module.nominal_effort, places=1)
    
    def test_calculate_function_points(self):
        module: Module = Module("<--test-->")
        
        counts = {
            "EI": (5, 10, 2),
            "EO":  (3, 8, 1),
            "ILF": (6, 17, 8),
            "EIF": (10, 10, 5),
            "EQ":  (2, 5, 0),
        }
        
        module.calculate_function_points(counts)
        self.assertEqual(654, module.function_points)

    def test_function_points_to_ksloc(self):
        module: Module = Module("<--test-->")
        module.function_points = 100
        module.language = "C"
        module.function_points_to_sloc()
        self.assertEqual(12_800, module.sloc)

    def test_module_encoder(self):
        module: Module = Module("Module 1")
        encoded = ModuleEncoder().default(module)
        with open('test_module.json', 'w') as file:
            json.dump(json.dumps(encoded,
                                 sort_keys=False,
                                 indent=4,
                                 ),
                      file)



if __name__ == "__main__":
    unittest.main()
