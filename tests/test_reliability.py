import unittest

from src.digital_ie.reliability import (
    exponential_model,
    inherent_availability,
    k_out_of_n_reliability,
    observed_metrics,
    observed_mttf,
    operational_availability,
    parallel_reliability,
    series_reliability,
    weibull_model,
    zero_failure_binomial_sample_size,
    zero_failure_exponential_test_time,
)


class ReliabilityMetricTests(unittest.TestCase):
    def test_observed_repairable_metrics(self):
        result = observed_metrics(1000, 4, 20)
        self.assertEqual(result["mtbf"], 250)
        self.assertEqual(result["mttr"], 5)
        self.assertAlmostEqual(result["failure_rate"], 0.004)
        self.assertAlmostEqual(result["observed_inherent_availability"], 1000 / 1020)
        self.assertAlmostEqual(inherent_availability(250, 5), 250 / 255)
        self.assertAlmostEqual(operational_availability(1000, 30), 1000 / 1030)
        self.assertEqual(observed_mttf(1000, 4), 250)

    def test_zero_failures_are_not_infinite_mtbf(self):
        result = observed_metrics(1000, 0)
        self.assertIsNone(result["mtbf"])
        self.assertEqual(result["failure_rate"], 0)
        self.assertIsNone(observed_mttf(1000, 0))
        with self.assertRaises(ValueError):
            observed_metrics(0, 1)
        with self.assertRaises(ValueError):
            observed_metrics(1000, 0, 5)

    def test_weibull_singular_hazard_is_receipt_safe(self):
        result = weibull_model(0, scale=1000, shape=0.5)
        self.assertIsNone(result["hazard"])
        self.assertIsNone(result["pdf"])


class LifeModelTests(unittest.TestCase):
    def test_exponential_reference_values(self):
        result = exponential_model(100, mttf=1000)
        self.assertAlmostEqual(result["reliability"], 0.9048374180359595)
        self.assertEqual(result["failure_rate"], 0.001)
        self.assertEqual(result["cumulative_hazard"], 0.1)
        with self.assertRaises(ValueError):
            exponential_model(100, failure_rate=0.001, mttf=1000)

    def test_weibull_shape_one_matches_exponential(self):
        weibull = weibull_model(100, scale=1000, shape=1)
        exponential = exponential_model(100, mttf=1000)
        self.assertAlmostEqual(weibull["reliability"], exponential["reliability"])
        self.assertAlmostEqual(weibull["hazard"], exponential["hazard"])
        self.assertAlmostEqual(weibull["mean_life"], 1000)


class SystemAndDemonstrationTests(unittest.TestCase):
    def test_series_parallel_and_k_out_of_n(self):
        self.assertAlmostEqual(series_reliability([0.9, 0.8]), 0.72)
        self.assertAlmostEqual(parallel_reliability([0.9, 0.8]), 0.98)
        self.assertAlmostEqual(k_out_of_n_reliability([0.9, 0.8, 0.7], 2), 0.902)
        self.assertAlmostEqual(k_out_of_n_reliability([0.9, 0.8], 1), 0.98)
        self.assertAlmostEqual(k_out_of_n_reliability([0.9, 0.8], 2), 0.72)

    def test_zero_failure_demonstration(self):
        self.assertEqual(zero_failure_binomial_sample_size(0.9, 0.9), 22)
        self.assertAlmostEqual(
            zero_failure_exponential_test_time(1000, 0.9),
            2302.585092994046,
        )


if __name__ == "__main__":
    unittest.main()
