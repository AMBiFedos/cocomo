import unittest
from cocomo import *


class TestCocomo(unittest.TestCase):
    def test_schedule_estimate_avg(self):
        root: CsciParent = CsciParent("Test")
        csci: CsciChild = CsciChild("Test CSCI", root)
        csci.size = 100
        csci.em_prod = 1.0
        csci.sf_sum = 24.0
        
        est: float = csci.schedule_estimate()
        self.assertAlmostEqual(586.61, est, places=2)

    def test_calculate_ufp(self):
        
        counts = {
            "EI": (5, 10, 2),
            "EO":  (3, 8, 1),
            "ILF": (6, 17, 8),
            "EIF": (10, 10, 5),
            "EQ":  (2, 5, 0),
        }
        
        ufp: int = calculate_ufp(counts)
        self.assertEqual(654, ufp)

    def test_ufp_to_sloc(self):
        sloc: int = ufp_to_ksloc(100, "C")
        self.assertEqual(12_800, sloc)




if __name__ == "__main__":
    unittest.main()
