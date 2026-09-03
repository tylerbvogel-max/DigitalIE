import unittest

from src.digital_ie.production import (
    flow_metrics,
    line_balance,
    mm1_queue,
    mmc_queue,
    overall_equipment_effectiveness,
    production_pace,
    rolled_throughput_yield,
    unit_learning_curve,
)


class ProductionCalculationTests(unittest.TestCase):
    def test_production_pace(self):
        result = production_pace(420, 100, 8, installed_parallel_resources=1)
        self.assertEqual(result.takt_time, 4.2)
        self.assertEqual(result.demonstrated_capacity, 52.5)
        self.assertEqual(result.minimum_parallel_resources, 2)
        self.assertEqual(result.staffing_gap, 1)

    def test_line_balance(self):
        result = line_balance([[2, 3], [4], [2, 2]], 480)
        self.assertEqual(result.station_loads, (5, 4, 4))
        self.assertEqual(result.cycle_time, 5)
        self.assertAlmostEqual(result.line_efficiency, 13 / 15)
        self.assertEqual(result.output_capacity, 96)

    def test_oee_factors_reconcile_to_fully_productive_time(self):
        result = overall_equipment_effectiveness(480, 420, 0.5, 800, 760)
        self.assertEqual(result.availability, 0.875)
        self.assertAlmostEqual(result.performance, 400 / 420)
        self.assertEqual(result.quality, 0.95)
        self.assertAlmostEqual(result.oee, 380 / 480)
        self.assertEqual(result.fully_productive_time, 380)

    def test_oee_rejects_impossible_performance(self):
        with self.assertRaisesRegex(ValueError, "performance exceeds"):
            overall_equipment_effectiveness(480, 300, 0.5, 700, 650)

    def test_littles_law_and_pce(self):
        result = flow_metrics(wip=120, throughput=10, value_added_time=2)
        self.assertEqual(result.implied_lead_time, 12)
        self.assertAlmostEqual(result.process_cycle_efficiency, 1 / 6)
        with self.assertRaises(ValueError):
            flow_metrics(wip=1, throughput=1, lead_time=1)

    def test_rolled_throughput_yield(self):
        result = rolled_throughput_yield([0.99, 0.98, 0.97])
        self.assertAlmostEqual(result["rolled_throughput_yield"], 0.99 * 0.98 * 0.97)

    def test_mm1_matches_closed_form(self):
        result = mm1_queue(4, 5)
        self.assertAlmostEqual(result.utilization, 0.8)
        self.assertAlmostEqual(result.average_queue_count, 3.2)
        self.assertAlmostEqual(result.average_system_count, 4)
        self.assertAlmostEqual(result.average_system_time, 1)

    def test_mmc_two_server_reference_case(self):
        result = mmc_queue(2, 1.5, 2)
        self.assertAlmostEqual(result.utilization, 2 / 3)
        self.assertAlmostEqual(result.probability_wait, 8 / 15)
        self.assertAlmostEqual(result.average_queue_count, 16 / 15)
        self.assertAlmostEqual(result.average_system_time, 1.2)

    def test_queues_fail_closed_when_unstable(self):
        with self.assertRaises(ValueError):
            mm1_queue(5, 5)
        with self.assertRaises(ValueError):
            mmc_queue(4, 2, 2)

    def test_unit_learning_curve(self):
        result = unit_learning_curve(100, 0.8, 4)
        self.assertAlmostEqual(result.unit_values[0], 100)
        self.assertAlmostEqual(result.unit_values[1], 80)
        self.assertAlmostEqual(result.unit_values[3], 64)
        self.assertAlmostEqual(result.total_value, sum(result.unit_values))


if __name__ == "__main__":
    unittest.main()
