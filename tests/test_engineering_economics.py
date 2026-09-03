import unittest

from src.digital_ie.engineering_economics import (
    break_even_units,
    equivalent_annual_value,
    future_value,
    internal_rate_of_return,
    life_cycle_cost,
    make_buy_analysis,
    net_present_value,
    npv_rate_sensitivity,
    payback_period,
    present_value,
)


class TimeValueTests(unittest.TestCase):
    def test_single_amount_and_npv(self):
        self.assertAlmostEqual(future_value(1000, 0.05, 3), 1157.625)
        self.assertAlmostEqual(present_value(1157.625, 0.05, 3), 1000)
        self.assertAlmostEqual(net_present_value([-1000, 600, 600], 0.1), 41.32231404958668)

    def test_equivalent_annual_value(self):
        self.assertAlmostEqual(equivalent_annual_value(1000, 0, 4), 250)
        self.assertAlmostEqual(equivalent_annual_value(1000, 0.1, 3), 402.1148036253773)

    def test_simple_and_discounted_payback(self):
        flows = [-1000, 400, 400, 400]
        self.assertEqual(payback_period(flows), 2.5)
        self.assertIsNone(payback_period(flows, 0.2))

    def test_bracketed_irr(self):
        result = internal_rate_of_return([-1000, 600, 600], 0, 1)
        self.assertAlmostEqual(net_present_value([-1000, 600, 600], result), 0, places=7)
        with self.assertRaisesRegex(ValueError, "not bracketed"):
            internal_rate_of_return([-1000, 100, 100], 0, 0.1)


class DecisionEconomicTests(unittest.TestCase):
    def test_break_even_and_make_buy(self):
        self.assertEqual(break_even_units(10_000, 100, 60), 250)
        self.assertIsNone(break_even_units(10_000, 50, 60))
        result = make_buy_analysis(1000, 20_000, 30, 60)
        self.assertEqual(result["make_total_cost"], 50_000)
        self.assertEqual(result["buy_total_cost"], 60_000)
        self.assertAlmostEqual(result["crossover_quantity"], 2000 / 3)
        self.assertEqual(result["lower_relevant_cost"], "make")

    def test_lifecycle_cost_and_sensitivity(self):
        costs = [1000, 100, 100]
        self.assertAlmostEqual(life_cycle_cost(costs, 0.1), 1173.5537190082644)
        sensitivity = npv_rate_sensitivity([-1000, 600, 600], [0, 0.1])
        self.assertEqual(sensitivity["0"], 200)
        self.assertAlmostEqual(sensitivity["0.10000000000000001"], 41.32231404958668)


if __name__ == "__main__":
    unittest.main()
