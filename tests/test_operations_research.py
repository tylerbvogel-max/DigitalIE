import unittest

from src.digital_ie.operations_research import (
    bounded_assignment,
    facility_center_of_gravity,
    single_machine_sequence,
    weighted_decision_scores,
)


class OperationsResearchTests(unittest.TestCase):
    def test_center_of_gravity(self):
        result = facility_center_of_gravity([(0, 0), (10, 0), (0, 10)], [1, 2, 1])
        self.assertEqual(result, {"x": 5, "y": 2.5, "total_weight": 4})

    def test_weighted_scoring_normalizes_weights(self):
        result = weighted_decision_scores(
            ["A", "B"], [[8, 4], [6, 9]], [3, 1]
        )
        self.assertEqual(result["normalized_weights"], (0.75, 0.25))
        self.assertEqual(result["ranking"], ("A", "B"))

    def test_bounded_assignment_finds_global_minimum(self):
        result = bounded_assignment([[9, 2, 7], [6, 4, 3], [5, 8, 1]])
        self.assertEqual(result.assignments, ((0, 1), (1, 0), (2, 2)))
        self.assertEqual(result.total_cost, 9)
        self.assertEqual(result.alternatives_evaluated, 6)

    def test_assignment_limit_is_explicit(self):
        with self.assertRaisesRegex(ValueError, "eight rows"):
            bounded_assignment([[1] * 9 for _ in range(9)])

    def test_sequence_rules_and_metrics(self):
        spt = single_machine_sequence(["A", "B", "C"], [5, 2, 3], [6, 8, 4], "spt")
        self.assertEqual(spt.order, ("B", "C", "A"))
        self.assertEqual(spt.completion_times, (2, 5, 10))
        self.assertEqual(spt.tardiness, (0, 1, 4))
        self.assertEqual(spt.jobs_late, 2)
        edd = single_machine_sequence(["A", "B", "C"], [5, 2, 3], [6, 8, 4], "edd")
        self.assertEqual(edd.order, ("C", "A", "B"))


if __name__ == "__main__":
    unittest.main()
