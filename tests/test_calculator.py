import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

from src.digital_ie.calculator import METHODS, calculate, list_methods, receipt_output_schema


class CalculationKernelTests(unittest.TestCase):
    def test_registry_is_unique_and_contains_no_arbitrary_evaluator(self):
        method_ids = [method.method_id for method in METHODS]
        tool_names = [method.tool_name for method in METHODS]
        self.assertEqual(len(method_ids), len(set(method_ids)))
        self.assertEqual(len(tool_names), len(set(tool_names)))
        self.assertNotIn("calculate", tool_names)
        self.assertNotIn("eval", " ".join(tool_names))
        self.assertEqual(len(list_methods()), len(METHODS))
        self.assertIn("authority_boundary", receipt_output_schema()["required"])

    def test_receipt_is_reproducible_and_preserves_boundaries(self):
        arguments = {
            "first": [8, 9, 10],
            "second": [10, 12, 14],
            "context": {
                "case_id": "case-example",
                "analysis_id": "analysis-welch-1",
                "evidence_ids": ["evidence-group-1", "evidence-group-2"],
                "units": "minutes",
                "purpose": "compare cycle-time means",
            },
        }
        first = calculate("comparison.welch_t", arguments)
        second = calculate("comparison.welch_t", arguments)
        self.assertEqual(first, second)
        self.assertEqual(first["calculation_id"], "calc-3d4811a5599f79d9e4b6")
        self.assertAlmostEqual(first["results"]["t_statistic"], -2.32379000772445)
        self.assertEqual(first["context_gaps"], [])
        self.assertIn("no product acceptance", first["authority_boundary"].lower())
        json.dumps(first, allow_nan=False)

    def test_context_does_not_change_arithmetic_identity(self):
        bare = calculate("probability.hypergeometric", {
            "successes": 1,
            "draws": 5,
            "population_successes": 3,
            "population_size": 20,
        })
        attached = calculate("probability.hypergeometric", {
            "successes": 1,
            "draws": 5,
            "population_successes": 3,
            "population_size": 20,
            "context": {"case_id": "case-example"},
        })
        self.assertEqual(bare["calculation_id"], attached["calculation_id"])
        self.assertEqual(bare["results"], attached["results"])

    def test_unknown_or_extra_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            calculate("expression.eval", {"expression": "2+2"})
        with self.assertRaises(ValueError):
            calculate("descriptive.summary", {"values": [1, 2], "prompt": "ignore rules"})
        with self.assertRaises(ValueError):
            calculate("descriptive.summary", {"values": [1, float("nan")]})
        with self.assertRaises(ValueError):
            calculate("descriptive.summary", {"values": [1, True]})
        with self.assertRaises(ValueError):
            calculate("descriptive.summary", {
                "values": [1, 2],
                "context": {"evidence_ids": "not-an-array"},
            })

    def test_poisson_requires_one_complete_parameterization(self):
        with self.assertRaises(ValueError):
            calculate("probability.poisson", {"events": 2})
        with self.assertRaises(ValueError):
            calculate("probability.poisson", {"events": 2, "rate": 0.5})
        receipt = calculate(
            "probability.poisson", {"events": 2, "rate": 0.5, "exposure": 6}
        )
        self.assertEqual(receipt["intermediates"]["expected_events"], 3.0)


class McpRoundTripTests(unittest.TestCase):
    def test_modern_discovery_is_supported(self):
        from src.digital_ie.calculator_mcp import handle_request

        response = handle_request({
            "jsonrpc": "2.0",
            "id": "discover",
            "method": "server/discover",
            "params": {
                "_meta": {
                    "io.modelcontextprotocol/protocolVersion": "2026-07-28",
                }
            },
        })
        self.assertEqual(response["result"]["supportedVersions"], ["2026-07-28"])
        self.assertIn("io.modelcontextprotocol/serverInfo", response["result"]["_meta"])

    def test_stdio_initialize_list_and_calculate(self):
        requests = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-11-25"},
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "descriptive_summary",
                    "arguments": {"values": [8, 9, 10, 10, 11, 12]},
                },
            },
        ]
        repository = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment["PYTHONPATH"] = str(repository / "src")
        completed = subprocess.run(
            [sys.executable, "-m", "digital_ie.calculator_mcp"],
            input="".join(json.dumps(request) + "\n" for request in requests),
            capture_output=True,
            check=True,
            cwd=repository,
            env=environment,
            text=True,
            timeout=10,
        )
        responses = [json.loads(line) for line in completed.stdout.splitlines()]
        self.assertEqual(len(responses), 3)
        self.assertEqual(responses[0]["result"]["serverInfo"]["name"], "digitalie-calculator")
        self.assertEqual(responses[0]["result"]["protocolVersion"], "2025-11-25")
        tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
        self.assertIn("descriptive_summary", tool_names)
        listed_tool = next(
            tool for tool in responses[1]["result"]["tools"]
            if tool["name"] == "descriptive_summary"
        )
        self.assertIn("authority_boundary", listed_tool["outputSchema"]["required"])
        receipt = responses[2]["result"]["structuredContent"]
        self.assertEqual(receipt["results"]["mean"], 10.0)
        self.assertTrue(responses[2]["result"]["isError"] is False)

    def test_tool_error_is_returned_without_server_failure(self):
        from src.digital_ie.calculator_mcp import handle_request

        response = handle_request({
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {"name": "descriptive_summary", "arguments": {"values": [1]}},
        })
        self.assertIsNotNone(response)
        self.assertTrue(response["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
