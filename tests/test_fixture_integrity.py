import json
import unittest
from pathlib import Path

from src.digital_ie.integrity import verified_hypothesis_is_defensible


FIXTURE = Path(__file__).parents[1] / "fixtures" / "assembly-torque-failure"


class FixtureIntegrityTests(unittest.TestCase):
    def test_case_uses_portable_identifier_and_control_phase(self):
        case = json.loads((FIXTURE / "case.json").read_text())
        self.assertEqual(case["id"], "DIE-2026-0001")
        self.assertEqual(case["status"], "control")

    def test_verified_cause_has_full_evidence_chain(self):
        evidence = json.loads((FIXTURE / "evidence.json").read_text())
        hypotheses = json.loads((FIXTURE / "hypotheses.json").read_text())
        ids = {item["id"] for item in evidence}
        verified = next(item for item in hypotheses if item["status"] == "verified")
        self.assertTrue(verified_hypothesis_is_defensible(verified, ids))

    def test_missing_approval_blocks_verified_claim(self):
        claim = {"status": "verified", "evidence_ids": ["E-001"], "validation_test_id": "T-003"}
        self.assertFalse(verified_hypothesis_is_defensible(claim, {"E-001"}))
