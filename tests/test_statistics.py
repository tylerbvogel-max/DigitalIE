import math
import unittest

from src.digital_ie.statistics import (
    chi_square_independence,
    mean,
    one_proportion_z_statistic,
    one_way_anova,
    paired_t_statistic,
    sample_standard_deviation,
    sample_variance,
    simple_linear_regression,
    standard_error_mean,
    two_proportion_z_statistic,
    welch_t_statistic,
    wilson_proportion_interval,
)


class DescriptiveStatisticsTests(unittest.TestCase):
    def test_documented_cycle_time_example(self):
        values = [8, 9, 10, 10, 11, 12]
        self.assertEqual(mean(values), 10.0)
        self.assertEqual(sample_variance(values), 2.0)
        self.assertAlmostEqual(sample_standard_deviation(values), math.sqrt(2))
        self.assertAlmostEqual(standard_error_mean(values), math.sqrt(2) / math.sqrt(6))


class ComparativeStatisticsTests(unittest.TestCase):
    def test_paired_t_uses_within_pair_differences(self):
        result = paired_t_statistic([10, 12, 11, 13], [9, 10, 10, 10])
        self.assertAlmostEqual(result, -3.5 / math.sqrt(11 / 12))

    def test_welch_t_reports_statistic_and_fractional_degrees_freedom(self):
        statistic, degrees_freedom = welch_t_statistic([8, 9, 10], [10, 12, 14])
        self.assertAlmostEqual(statistic, -3 / math.sqrt(5 / 3))
        self.assertAlmostEqual(degrees_freedom, 2.9411764705882346)

    def test_proportion_statistics(self):
        self.assertAlmostEqual(one_proportion_z_statistic(12, 100, 0.2), -2.0)
        self.assertAlmostEqual(two_proportion_z_statistic(18, 100, 10, 100), 1.6302782918784444)
        lower, upper = wilson_proportion_interval(2, 20, 1.96)
        self.assertAlmostEqual(lower, 0.027865893984153206)
        self.assertAlmostEqual(upper, 0.30103820641179335)

    def test_documented_chi_square_example(self):
        statistic, degrees_freedom = chi_square_independence([[18, 2], [12, 8]])
        self.assertAlmostEqual(statistic, 4.8)
        self.assertEqual(degrees_freedom, 1)

    def test_documented_anova_example(self):
        result = one_way_anova([[8, 9, 10], [11, 12, 13], [9, 10, 11]])
        self.assertAlmostEqual(result.between_sum_squares, 14.0)
        self.assertAlmostEqual(result.within_sum_squares, 6.0)
        self.assertAlmostEqual(result.f_statistic, 7.0)


class RegressionTests(unittest.TestCase):
    def test_documented_simple_regression_example(self):
        result = simple_linear_regression([1, 2, 3, 4, 5], [2, 4, 5, 4, 8])
        self.assertAlmostEqual(result.intercept, 1.0)
        self.assertAlmostEqual(result.slope, 1.2)
        self.assertAlmostEqual(result.correlation, math.sqrt(0.75))
        self.assertAlmostEqual(result.determination, 0.75)
        self.assertAlmostEqual(result.sse, 4.8)
        self.assertAlmostEqual(result.ssr, 14.4)
        self.assertAlmostEqual(result.mse, 1.6)
        self.assertAlmostEqual(result.slope_standard_error, 0.4)
        self.assertAlmostEqual(result.slope_t, 3.0)

    def test_regression_rejects_constant_predictor(self):
        with self.assertRaises(ValueError):
            simple_linear_regression([1, 1, 1], [2, 3, 4])
