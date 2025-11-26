import unittest
from cocomo import *


class TestCocomo(unittest.TestCase):
    
    def test_module_estimate_schedule(self):
        module: Module = Module("<--test-->")
        module.ksloc = 100
        module.em_prod = 1.0
        scale_factor: float = 24.0
        
        module.estimate_schedule(scale_factor)
        self.assertAlmostEqual(586.61, module.nominal_schedule, places=2)

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
        module.function_points_to_ksloc()
        self.assertEqual(12_800, module.ksloc)




if __name__ == "__main__":
    unittest.main()
