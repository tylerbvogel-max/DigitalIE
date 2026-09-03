import unittest

from src.digital_ie.calculator import calculate
from src.digital_ie.calculator_mcp import handle_request
from src.digital_ie.evm import (
    forecast_at_completion,
    labor_cost_variance,
    material_cost_variance,
    performance_snapshot,
    reconcile_periods,
    schedule_execution,
)


class EvmPerformanceTests(unittest.TestCase):
    def test_performance_snapshot(self):
        result = performance_snapshot(1000, 900, 950, 5000, management_etc=4200)
        self.assertEqual(result.cost_variance, -50)
        self.assertEqual(result.schedule_variance, -100)
        self.assertAlmostEqual(result.cost_variance_percent, -50 / 9)
        self.assertEqual(result.schedule_variance_percent, -10)
        self.assertAlmostEqual(result.cost_performance_index, 900 / 950)
        self.assertEqual(result.schedule_performance_index, 0.9)
        self.assertEqual(result.percent_scheduled, 20)
        self.assertEqual(result.percent_complete, 18)
        self.assertEqual(result.percent_spent, 19)
        self.assertEqual(result.work_remaining, 4100)
        self.assertEqual(result.management_eac, 5150)
        self.assertEqual(result.variance_at_completion, -150)

    def test_zero_denominators_are_explicitly_undefined(self):
        result = performance_snapshot(0, 0, 0, 5000)
        self.assertIsNone(result.cost_variance_percent)
        self.assertIsNone(result.schedule_variance_percent)
        self.assertIsNone(result.cost_performance_index)
        self.assertIsNone(result.schedule_performance_index)

    def test_baseline_relationships_fail_closed(self):
        with self.assertRaises(ValueError):
            performance_snapshot(5100, 900, 950, 5000)
        with self.assertRaises(ValueError):
            performance_snapshot(1000, 5100, 950, 5000)


class EvmForecastTests(unittest.TestCase):
    def test_forecast_alternatives_and_tcpi(self):
        result = forecast_at_completion(
            1000,
            900,
            950,
            5000,
            management_etc=4200,
            recent_period_ev=[100, 120, 110],
            recent_period_ac=[110, 130, 120],
        )
        cumulative_cpi = 900 / 950
        cumulative_spi = 900 / 1000
        recent_cpi = 330 / 360
        self.assertAlmostEqual(result.cumulative_cpi, cumulative_cpi)
        self.assertAlmostEqual(result.cumulative_spi, cumulative_spi)
        self.assertAlmostEqual(result.recent_cpi, recent_cpi)
        self.assertAlmostEqual(result.eac_cpi, 950 + 4100 / cumulative_cpi)
        self.assertAlmostEqual(result.eac_composite, 950 + 4100 / (cumulative_cpi * cumulative_spi))
        self.assertAlmostEqual(result.eac_composite, 5758.641975308642)
        self.assertAlmostEqual(result.eac_recent_cpi, 950 + 4100 / recent_cpi)
        self.assertEqual(result.eac_management, 5150)
        self.assertAlmostEqual(result.tcpi_bac, 4100 / 4050)
        self.assertAlmostEqual(result.tcpi_management_eac, 4100 / 4200)

    def test_recent_period_series_must_align(self):
        with self.assertRaises(ValueError):
            forecast_at_completion(1000, 900, 950, 5000, recent_period_ev=[100])


class EvmIntegrityAndDecompositionTests(unittest.TestCase):
    def test_period_reconciliation(self):
        result = reconcile_periods(
            [200, 300, 500],
            [180, 290, 430],
            [190, 310, 450],
            1000,
            900,
            950,
        )
        self.assertTrue(result["within_tolerance"])
        self.assertEqual(result["ev_reconciliation_delta"], 0)
        mismatch = reconcile_periods([200, 300], [180, 290], [190, 310], 501, 470, 500)
        self.assertFalse(mismatch["within_tolerance"])
        self.assertEqual(mismatch["pv_reconciliation_delta"], 1)

    def test_schedule_execution_metrics(self):
        result = schedule_execution(18, 20, 7, 10)
        self.assertEqual(result["baseline_execution_index"], 0.9)
        self.assertEqual(result["hit_miss_task_percent"], 70)
        with self.assertRaises(ValueError):
            schedule_execution(21, 20, 7, 10)

    def test_labor_variance_reconciles_to_earned_minus_actual_cost(self):
        result = labor_cost_variance(100, 110, 80, 90)
        self.assertEqual(result.rate_or_price_variance, -900)
        self.assertEqual(result.volume_or_usage_variance, -1000)
        self.assertEqual(result.total_cost_variance, 80 * 100 - 90 * 110)

    def test_material_variance_reconciles_to_earned_minus_actual_cost(self):
        result = material_cost_variance(50, 55, 100, 110)
        self.assertEqual(result.rate_or_price_variance, -550)
        self.assertEqual(result.volume_or_usage_variance, -500)
        self.assertEqual(result.total_cost_variance, 100 * 50 - 110 * 55)

    def test_calculator_receipt_uses_evm_boundaries(self):
        receipt = calculate("program.evm_snapshot", {
            "status_date": "2026-08-31",
            "baseline_id": "PMB-004",
            "scope_id": "CA-1200",
            "value_units": "USD",
            "pv": 1000,
            "ev": 900,
            "ac": 950,
            "bac": 5000,
        })
        self.assertEqual(receipt["results"]["cost_variance"], -50)
        self.assertIn("baseline scope", receipt["assumptions_not_established"][0])
        self.assertIn("no EVMS compliance", receipt["authority_boundary"])

    def test_empty_evm_context_identifier_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "minimum length"):
            calculate("program.evm_snapshot", {
                "status_date": "2026-08-31",
                "baseline_id": "",
                "scope_id": "CA-1200",
                "value_units": "USD",
                "pv": 1000,
                "ev": 900,
                "ac": 950,
                "bac": 5000,
            })

    def test_evm_tool_round_trip(self):
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 7,
            "method": "tools/call",
            "params": {
                "name": "program_evm_snapshot",
                "arguments": {
                    "status_date": "2026-08-31",
                    "baseline_id": "PMB-004",
                    "scope_id": "CA-1200",
                    "value_units": "USD",
                    "pv": 1000,
                    "ev": 900,
                    "ac": 950,
                    "bac": 5000,
                },
            },
        })
        self.assertFalse(response["result"]["isError"])
        self.assertEqual(
            response["result"]["structuredContent"]["results"]["cost_variance"],
            -50,
        )


if __name__ == "__main__":
    unittest.main()
