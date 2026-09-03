import unittest

from src.digital_ie.schedule_risk import (
    critical_path,
    pert_estimate,
    simulate_cost,
    simulate_schedule,
)


class CriticalPathTests(unittest.TestCase):
    def setUp(self):
        self.network = [
            {"id": "A", "duration": 3, "predecessors": []},
            {"id": "B", "duration": 4, "predecessors": ["A"]},
            {"id": "C", "duration": 2, "predecessors": ["A"]},
            {"id": "D", "duration": 5, "predecessors": ["B", "C"]},
        ]

    def test_forward_backward_pass_and_float(self):
        result = critical_path(self.network)
        self.assertEqual(result["project_duration"], 12)
        self.assertEqual(result["critical_activity_ids"], ["A", "B", "D"])
        rows = {row["id"]: row for row in result["activities"]}
        self.assertEqual(rows["C"]["total_float"], 2)
        self.assertEqual(rows["C"]["free_float"], 2)
        self.assertEqual(rows["D"]["late_finish"], 12)

    def test_invalid_logic_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "missing predecessor"):
            critical_path([{"id": "A", "duration": 1, "predecessors": ["X"]}])
        with self.assertRaisesRegex(ValueError, "cycle"):
            critical_path([
                {"id": "A", "duration": 1, "predecessors": ["B"]},
                {"id": "B", "duration": 1, "predecessors": ["A"]},
            ])

    def test_pert_estimate(self):
        result = pert_estimate(2, 5, 14)
        self.assertEqual(result["expected_duration"], 6)
        self.assertEqual(result["standard_deviation"], 2)
        self.assertEqual(result["variance"], 4)
        with self.assertRaises(ValueError):
            pert_estimate(5, 2, 14)


class RiskSimulationTests(unittest.TestCase):
    def test_schedule_simulation_is_seeded_and_bounded(self):
        activities = [
            {
                "id": "A",
                "optimistic": 1,
                "most_likely": 2,
                "pessimistic": 4,
                "predecessors": [],
            },
            {
                "id": "B",
                "optimistic": 2,
                "most_likely": 3,
                "pessimistic": 5,
                "predecessors": ["A"],
            },
        ]
        first = simulate_schedule(activities, 250, 42)
        second = simulate_schedule(activities, 250, 42)
        self.assertEqual(first, second)
        self.assertLessEqual(first["p50_duration"], first["p90_duration"])
        self.assertEqual(first["criticality_index"], {"A": 1.0, "B": 1.0})
        with self.assertRaises(ValueError):
            simulate_schedule(activities, 100_001, 42)

    def test_cost_simulation_is_seeded_and_ordered(self):
        elements = [
            {
                "id": "tooling",
                "minimum": 90,
                "most_likely": 100,
                "maximum": 130,
                "risk_probability": 0.2,
                "risk_impact": 50,
            }
        ]
        first = simulate_cost(elements, 500, 7)
        second = simulate_cost(elements, 500, 7)
        self.assertEqual(first, second)
        self.assertLessEqual(first["p50_cost"], first["p95_cost"])
        self.assertGreater(first["mean_cost"], 90)


if __name__ == "__main__":
    unittest.main()
