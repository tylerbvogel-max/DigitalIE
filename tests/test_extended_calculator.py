import json
import unittest

from src.digital_ie.calculator import METHODS, calculate
from src.digital_ie.calculator_mcp import handle_request


class ExtendedRegistryTests(unittest.TestCase):
    def test_all_calculation_packs_are_registered(self):
        method_ids = {item.method_id for item in METHODS}
        self.assertEqual(len(METHODS), 79)
        for expected in (
            "quality.gage_rr_crossed",
            "production.queue_mmc",
            "supply.mrp_netting",
            "operations.bounded_assignment",
            "program.schedule_simulation",
            "reliability.weibull",
            "economics.irr",
        ):
            self.assertIn(expected, method_ids)

    def test_registry_contracts_are_closed_unique_and_serializable(self):
        tool_names = [item.tool_name for item in METHODS]
        method_ids = [item.method_id for item in METHODS]
        self.assertEqual(len(tool_names), len(set(tool_names)))
        self.assertEqual(len(method_ids), len(set(method_ids)))
        for contract in METHODS:
            self.assertFalse(contract.input_schema.get("additionalProperties", True))
            self.assertTrue(contract.version)
            json.dumps(contract.public_description(), allow_nan=False)

    def test_representative_pack_receipts_are_serializable(self):
        examples = {
            "quality.capability": {
                "mean_value": 10, "within_sigma": 1, "overall_sigma": 1.2,
                "lsl": 6, "usl": 14,
            },
            "production.oee": {
                "planned_production_time": 480, "run_time": 420,
                "ideal_cycle_time": 1, "total_count": 400, "good_count": 380,
            },
            "supply.eoq": {
                "annual_demand": 10000, "order_cost": 50,
                "annual_holding_cost_per_unit": 2,
            },
            "operations.bounded_assignment": {"cost_matrix": [[9, 2], [3, 8]]},
            "program.critical_path": {
                "activities": [
                    {"id": "A", "duration": 2},
                    {"id": "B", "duration": 3, "predecessors": ["A"]},
                ],
            },
            "reliability.weibull": {"time": 100, "scale": 200, "shape": 2},
            "economics.npv": {"cash_flows": [-100, 60, 60], "rate": 0.1},
        }
        receipts = {name: calculate(name, inputs) for name, inputs in examples.items()}
        json.dumps(receipts, allow_nan=False)
        self.assertAlmostEqual(receipts["quality.capability"]["results"]["cp"], 4 / 3)
        self.assertAlmostEqual(receipts["production.oee"]["results"]["oee"], 19 / 24)
        self.assertAlmostEqual(receipts["supply.eoq"]["results"]["economic_order_quantity"], 500000**0.5)
        self.assertEqual(receipts["operations.bounded_assignment"]["results"]["total_cost"], 5)
        self.assertEqual(receipts["program.critical_path"]["results"]["project_duration"], 5)
        self.assertAlmostEqual(receipts["reliability.weibull"]["results"]["reliability"], 0.7788007830714049)
        self.assertAlmostEqual(receipts["economics.npv"]["results"]["net_present_value"], 4.132231404958667)

    def test_simulation_receipt_is_seed_reproducible(self):
        arguments = {
            "activities": [
                {"id": "A", "optimistic": 1, "most_likely": 2, "pessimistic": 4},
                {
                    "id": "B", "optimistic": 2, "most_likely": 3,
                    "pessimistic": 5, "predecessors": ["A"],
                },
            ],
            "iterations": 100,
            "seed": 42,
        }
        first = calculate("program.schedule_simulation", arguments)
        second = calculate("program.schedule_simulation", arguments)
        self.assertEqual(first, second)
        self.assertEqual(first["results"]["iterations"], 100)
        self.assertEqual(first["results"]["seed"], 42)

    def test_mcp_lists_and_calls_extended_method(self):
        listed = handle_request({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        names = {item["name"] for item in listed["result"]["tools"]}
        self.assertIn("reliability_series", names)
        response = handle_request({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "reliability_series",
                "arguments": {"component_reliabilities": [0.9, 0.8]},
            },
        })
        self.assertFalse(response["result"]["isError"])
        result = response["result"]["structuredContent"]
        self.assertAlmostEqual(result["results"]["system_reliability"], 0.72)
        self.assertIn("no schedule baseline", result["authority_boundary"])

    def test_closed_schema_rejects_extra_fields(self):
        with self.assertRaisesRegex(ValueError, "unexpected fields"):
            calculate("economics.npv", {
                "cash_flows": [-100, 120], "rate": 0.1, "approve_investment": True,
            })


if __name__ == "__main__":
    unittest.main()
