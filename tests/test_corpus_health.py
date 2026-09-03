import json
import unittest
from pathlib import Path

from src.digital_ie.corpus_health import broken_internal_links, missing_contract_fields


ROOT = Path(__file__).parents[1]


class CorpusHealthTests(unittest.TestCase):
    def test_json_documents_parse(self):
        for path in ROOT.rglob("*.json"):
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_internal_markdown_links_resolve(self):
        self.assertEqual(broken_internal_links(ROOT), [])

    def test_process_and_agent_contracts_are_complete(self):
        self.assertEqual(missing_contract_fields(ROOT), [])
