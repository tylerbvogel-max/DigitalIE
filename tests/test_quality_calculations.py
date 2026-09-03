import unittest
from math import sqrt

from src.digital_ie.quality import (
    c_chart,
    capability_indices,
    crossed_gage_rr_anova,
    individuals_moving_range,
    np_chart,
    p_chart,
    single_sampling_oc,
    tolerance_stack,
    two_level_full_factorial_effects,
    u_chart,
    xbar_r_chart,
    xbar_s_chart,
    yield_metrics,
)


class ControlChartTests(unittest.TestCase):
    def test_individuals_moving_range_matches_nist_example(self):
        values = [49.6, 47.6, 49.9, 51.3, 47.8, 51.2, 52.6, 52.4, 53.6, 52.1]
        result = individuals_moving_range(values)
        self.assertAlmostEqual(result["individual_center_line"], 50.81)
        self.assertAlmostEqual(result["moving_range_center_line"], 1.877777777777778)
        self.assertAlmostEqual(result["individual_upper_control_limit"], 55.80408983451537)
        self.assertAlmostEqual(result["individual_lower_control_limit"], 45.81591016548463)
        self.assertAlmostEqual(result["moving_range_upper_control_limit"], 6.1347)

    def test_xbar_r_uses_supplied_constants(self):
        result = xbar_r_chart(
            [[10, 12, 11], [9, 10, 11], [12, 13, 11]],
            a2=1.023,
            d3=0,
            d4=2.574,
            d2=1.693,
        )
        self.assertEqual(result["subgroup_means"], [11, 10, 12])
        self.assertEqual(result["xbar_center_line"], 11)
        self.assertAlmostEqual(result["xbar_upper_control_limit"], 13.046)
        self.assertAlmostEqual(result["range_upper_control_limit"], 5.148)
        self.assertAlmostEqual(result["estimated_within_sigma"], 2 / 1.693)

    def test_xbar_s_uses_sample_standard_deviation(self):
        result = xbar_s_chart(
            [[10, 12, 11], [9, 10, 11], [12, 13, 11]],
            a3=1.954,
            b3=0,
            b4=2.568,
        )
        self.assertEqual(result["standard_deviation_center_line"], 1)
        self.assertAlmostEqual(result["xbar_lower_control_limit"], 9.046)
        self.assertAlmostEqual(result["standard_deviation_upper_control_limit"], 2.568)

    def test_attribute_charts(self):
        p_result = p_chart([2, 4], [100, 200])
        self.assertAlmostEqual(p_result["center_line"], 0.02)
        self.assertNotEqual(
            p_result["upper_control_limits"][0],
            p_result["upper_control_limits"][1],
        )
        np_result = np_chart([2, 4], 100)
        self.assertEqual(np_result["center_line"], 3)
        c_result = c_chart([2, 4, 6])
        self.assertEqual(c_result["center_line"], 4)
        u_result = u_chart([2, 6], [100, 200])
        self.assertAlmostEqual(u_result["center_line"], 8 / 300)
        self.assertEqual(len(u_result["upper_control_limits"]), 2)

    def test_invalid_control_chart_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            p_chart([101], [100])
        with self.assertRaises(ValueError):
            xbar_r_chart([[1, 2], [1, 2, 3]], a2=1, d3=0, d4=2)


class QualityMetricTests(unittest.TestCase):
    def test_capability_separates_within_and_overall_variation(self):
        result = capability_indices(
            mean_value=10.2,
            within_sigma=0.5,
            overall_sigma=0.6,
            lsl=8,
            usl=12,
        )
        self.assertAlmostEqual(result["cp"], 4 / 3)
        self.assertAlmostEqual(result["cpk"], 1.2)
        self.assertAlmostEqual(result["pp"], 4 / 3.6)
        self.assertAlmostEqual(result["ppk"], 1.0)

    def test_yield_metrics(self):
        result = yield_metrics(
            units=100,
            defects=5,
            opportunities_per_unit=10,
            step_yields=[0.98, 0.97, 0.99],
            conforming_units=97,
        )
        self.assertEqual(result["unit_yield"], 0.97)
        self.assertEqual(result["defects_per_unit"], 0.05)
        self.assertEqual(result["defects_per_opportunity"], 0.005)
        self.assertEqual(result["defects_per_million_opportunities"], 5000)
        self.assertAlmostEqual(result["rolled_throughput_yield"], 0.98 * 0.97 * 0.99)

    def test_tolerance_stack(self):
        result = tolerance_stack([0.1, 0.2, 0.2])
        self.assertAlmostEqual(result["worst_case_tolerance"], 0.5)
        self.assertAlmostEqual(result["root_sum_square_tolerance"], 0.3)
        with self.assertRaises(ValueError):
            tolerance_stack([0.1, -0.2])


class MeasurementSamplingAndExperimentTests(unittest.TestCase):
    def test_crossed_gage_rr_returns_reconciled_components(self):
        data = [
            [[9.9, 10.1], [10.0, 10.2]],
            [[19.9, 20.1], [20.0, 20.2]],
            [[29.9, 30.1], [30.0, 30.2]],
        ]
        result = crossed_gage_rr_anova(data)
        self.assertAlmostEqual(result["repeatability_variance"], 0.02)
        self.assertAlmostEqual(result["operator_variance"], 0.005)
        self.assertAlmostEqual(result["part_operator_interaction_variance"], 0)
        self.assertEqual(result["part_degrees_of_freedom"], 2)
        self.assertEqual(result["repeatability_degrees_of_freedom"], 6)
        self.assertAlmostEqual(result["repeatability_mean_square"], 0.02)
        self.assertAlmostEqual(
            result["total_variance"],
            result["gage_rr_variance"] + result["part_to_part_variance"],
        )
        self.assertAlmostEqual(
            result["gage_rr_standard_deviation"],
            sqrt(result["gage_rr_variance"]),
        )

    def test_single_sampling_oc_matches_binomial_result(self):
        result = single_sampling_oc(10, 1, 0.1)
        expected = 0.9**10 + 10 * 0.1 * 0.9**9
        self.assertAlmostEqual(result["probability_of_acceptance"], expected)
        self.assertAlmostEqual(
            result["probability_of_acceptance"] + result["probability_of_rejection"],
            1,
        )

    def test_two_level_factorial_recovers_known_model(self):
        design = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
        responses = [6, 8, 10, 16]
        result = two_level_full_factorial_effects(design, responses, ["A", "B"])
        self.assertEqual(result["intercept"], 10)
        self.assertEqual(result["effects"], {"A": 6, "B": 4, "A:B": 2})

    def test_factorial_requires_complete_unique_design(self):
        with self.assertRaises(ValueError):
            two_level_full_factorial_effects(
                [[-1, -1], [-1, 1], [1, -1], [1, -1]],
                [1, 2, 3, 4],
                ["A", "B"],
            )


if __name__ == "__main__":
    unittest.main()
