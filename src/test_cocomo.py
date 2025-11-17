import unittest
from cocomo import *


class TestCocomo(unittest.TestCase):
    def test_schedule_estimate_avg(self):
        size: int = 100
        em_prod: float = 1.0
        sf_sum: float = 24.0
        
        est: float = schedule_estimate(size, em_prod, sf_sum)
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
