"""Dependency-free fitness checks for the Markdown corpus."""

from __future__ import annotations

import re
from pathlib import Path


LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PROCESS_SECTIONS = ("## Process contract", "**Decision gates:**", "**Measures:**")
AGENT_FIELDS = ("**Required records:**", "**May:**", "**Critics:**", "**Must escalate:**", "**Output:**")


def broken_internal_links(root: Path) -> list[str]:
    failures: list[str] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            clean = target.split("#", 1)[0]
            if not clean or "://" in clean or clean.startswith("mailto:"):
                continue
            resolved = (path.parent / clean).resolve()
            if not resolved.exists():
                failures.append(f"{path.relative_to(root)} -> {target}")
    return sorted(failures)


def missing_contract_fields(root: Path) -> list[str]:
    failures: list[str] = []
    for path in sorted((root / "processes").glob("[0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        missing = [field for field in PROCESS_SECTIONS if field not in text]
        if missing:
            failures.append(f"{path.relative_to(root)} missing {', '.join(missing)}")
    for path in sorted((root / "agents").glob("[0-9][0-9]-*.md")):
        text = path.read_text(encoding="utf-8")
        missing = [field for field in AGENT_FIELDS if field not in text]
        if missing:
            failures.append(f"{path.relative_to(root)} missing {', '.join(missing)}")
    return failures


def corpus_failures(root: Path) -> list[str]:
    return broken_internal_links(root) + missing_contract_fields(root)
