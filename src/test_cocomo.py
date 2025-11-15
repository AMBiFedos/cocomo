import unittest
from cocomo import *


class TestCocomo(unittest.TestCase):
    def test_schedule_estimate_avg(self):
        size: int = 100
        em_prod: float = 1.0
        sf_sum: float = 24.0
        
        est: float = schedule_estimate(size, em_prod, sf_sum)
        self.assertAlmostEqual(586.61, est, places=2)



if __name__ == "__main__":
    unittest.main()
