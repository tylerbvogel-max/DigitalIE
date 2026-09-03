import json
import unittest
from pathlib import Path

from src.digital_ie.corpus_health import (
    broken_internal_links,
    case_contract_mismatches,
    duplicate_local_titles,
    missing_contract_fields,
    unindexed_entries,
)


ROOT = Path(__file__).parents[1]


class CorpusHealthTests(unittest.TestCase):
    def test_json_documents_parse(self):
        for path in ROOT.rglob("*.json"):
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_schema_identifiers_use_one_stable_namespace(self):
        for path in (ROOT / "schemas").glob("*.json"):
            with self.subTest(path=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(
                    schema["$id"], f"https://digitalie.local/schemas/{path.name}"
                )

    def test_internal_markdown_links_resolve(self):
        self.assertEqual(broken_internal_links(ROOT), [])

    def test_process_and_agent_contracts_are_complete(self):
        self.assertEqual(missing_contract_fields(ROOT), [])

    def test_operational_entries_are_indexed(self):
        self.assertEqual(unindexed_entries(ROOT), [])

    def test_collection_titles_are_unique(self):
        self.assertEqual(duplicate_local_titles(ROOT), [])

    def test_case_schema_matches_process_and_lifecycle_definitions(self):
        self.assertEqual(case_contract_mismatches(ROOT), [])
