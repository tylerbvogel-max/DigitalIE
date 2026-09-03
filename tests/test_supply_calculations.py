import unittest
from math import sqrt

from src.digital_ie.supply import (
    economic_order_quantity,
    forecast_accuracy,
    moving_average,
    mrp_netting,
    reorder_point,
    simple_exponential_smoothing,
)


class SupplyCalculationTests(unittest.TestCase):
    def test_moving_average_alignment(self):
        result = moving_average([10, 12, 14, 16], 2)
        self.assertEqual(result["fitted_forecasts"], (None, None, 11, 13))
        self.assertEqual(result["next_forecast"], 15)

    def test_simple_exponential_smoothing(self):
        result = simple_exponential_smoothing([10, 14, 12], 0.5)
        self.assertEqual(result["fitted_forecasts"], (10, 10, 12))
        self.assertEqual(result["next_forecast"], 12)

    def test_forecast_accuracy_conventions(self):
        result = forecast_accuracy([100, 0, 120], [90, 5, 130])
        self.assertEqual(result.errors, (10, -5, -10))
        self.assertAlmostEqual(result.mean_error, -5 / 3)
        self.assertAlmostEqual(result.mad, 25 / 3)
        self.assertAlmostEqual(result.mape_percent, (0.1 + 10 / 120) / 2 * 100)
        self.assertEqual(result.mape_excluded_zero_actuals, 1)

    def test_eoq_balances_relevant_costs(self):
        result = economic_order_quantity(10_000, 50, 2)
        self.assertAlmostEqual(result.economic_order_quantity, sqrt(500_000))
        self.assertAlmostEqual(result.annual_ordering_cost, result.annual_cycle_stock_holding_cost)

    def test_reorder_point_independent_demand(self):
        result = reorder_point(100, 4, 10, 1.645)
        self.assertEqual(result["expected_lead_time_demand"], 400)
        self.assertEqual(result["lead_time_demand_standard_deviation"], 20)
        self.assertAlmostEqual(result["safety_stock"], 32.9)
        self.assertAlmostEqual(result["reorder_point"], 432.9)

    def test_lot_for_lot_mrp_and_release_offset(self):
        result = mrp_netting([0, 8, 6, 12], [0, 0, 2, 0], 10, 1)
        self.assertEqual(result.projected_available, (10, 2, 0, 0))
        self.assertEqual(result.net_requirements, (0, 0, 2, 12))
        self.assertEqual(result.planned_order_receipts, (0, 0, 2, 12))
        self.assertEqual(result.planned_order_releases, (0, 2, 12, 0))
        self.assertEqual(result.past_due_releases, ())

    def test_fixed_order_quantity_mrp_and_past_due_signal(self):
        result = mrp_netting([7, 7], [0, 0], 0, 1, fixed_order_quantity=10)
        self.assertEqual(result.planned_order_receipts, (10, 10))
        self.assertEqual(result.projected_available, (3, 6))
        self.assertEqual(result.past_due_releases, ({"receipt_period": 0, "quantity": 10},))


if __name__ == "__main__":
    unittest.main()
