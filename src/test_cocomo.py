import unittest
from cocomo import *


class TestCocomo(unittest.TestCase):
    
    def test_csci_child_estimate_schedule(self):
        child: CsciChild = CsciChild("Test CSCI")
        child.ksloc = 100
        child.em_prod = 1.0
        child.sf_sum = 24.0
        
        child.estimate_schedule()
        self.assertAlmostEqual(586.61, child.nominal_schedule, places=2)

    def test_calculate_function_points(self):
        child: CsciChild = CsciChild("Test CSCI")
        
        counts = {
            "EI": (5, 10, 2),
            "EO":  (3, 8, 1),
            "ILF": (6, 17, 8),
            "EIF": (10, 10, 5),
            "EQ":  (2, 5, 0),
        }
        
        child.calculate_function_points(counts)
        self.assertEqual(654, child.function_points)

    def test_function_points_to_ksloc(self):
        child: CsciChild = CsciChild("Test CSCI")
        child.function_points = 100
        child.language = "C"
        child.function_points_to_ksloc()
        self.assertEqual(12_800, child.ksloc)




if __name__ == "__main__":
    unittest.main()
