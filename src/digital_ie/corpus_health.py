"""Dependency-free fitness checks for the Markdown corpus."""

from __future__ import annotations

import json
import re
from pathlib import Path


LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PROCESS_SECTIONS = ("## Process contract", "**Decision gates:**", "**Measures:**")
AGENT_FIELDS = ("**Required records:**", "**May:**", "**Critics:**", "**Must escalate:**", "**Output:**")
INDEXED_ROOTS = ("agents", "framework", "operating-system", "processes")


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


def unindexed_entries(root: Path) -> list[str]:
    """Report operational Markdown files omitted from their local index."""
    collections = [root / name for name in INDEXED_ROOTS]
    collections.extend(path for path in (root / "playbooks").iterdir() if path.is_dir())
    failures: list[str] = []
    for directory in sorted(collections):
        index = directory / "README.md"
        if not index.exists():
            failures.append(f"{directory.relative_to(root)} missing README.md")
            continue
        index_text = index.read_text(encoding="utf-8")
        for path in sorted(directory.glob("*.md")):
            if path.name != "README.md" and path.name not in index_text:
                failures.append(f"{path.relative_to(root)} is absent from {index.relative_to(root)}")
    return failures


def duplicate_local_titles(root: Path) -> list[str]:
    """Report duplicate H1 titles within one collection directory."""
    by_directory: dict[Path, dict[str, list[Path]]] = {}
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        match = re.search(r"^#\s+(.+)$", path.read_text(encoding="utf-8"), re.MULTILINE)
        if match is None:
            continue
        title = match.group(1).strip().casefold()
        by_directory.setdefault(path.parent, {}).setdefault(title, []).append(path)
    failures: list[str] = []
    for titles in by_directory.values():
        for title, paths in titles.items():
            if len(paths) > 1:
                names = ", ".join(str(path.relative_to(root)) for path in sorted(paths))
                failures.append(f"duplicate local title '{title}': {names}")
    return sorted(failures)


def case_contract_mismatches(root: Path) -> list[str]:
    """Compare case-schema routes and states with their Markdown definitions."""
    schema = json.loads((root / "schemas" / "case.schema.json").read_text(encoding="utf-8"))
    properties = schema["properties"]
    declared_processes = set(properties["process"]["enum"])
    process_files = {
        path.stem[3:] for path in (root / "processes").glob("[0-9][0-9]-*.md")
    }
    failures: list[str] = []
    if declared_processes != process_files:
        failures.append(
            "case process enum mismatch: "
            f"schema-only={sorted(declared_processes - process_files)}, "
            f"files-only={sorted(process_files - declared_processes)}"
        )

    lifecycle = (root / "framework" / "case-lifecycle.md").read_text(encoding="utf-8")
    documented_states: set[str] = set()
    for line in lifecycle.splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|", line)
        if match is None or match.group(1) in ("State", "---"):
            continue
        state = re.sub(r"[^a-z0-9]+", "-", match.group(1).casefold()).strip("-")
        documented_states.add(state)
    declared_states = set(properties["status"]["enum"])
    if declared_states != documented_states:
        failures.append(
            "case status enum mismatch: "
            f"schema-only={sorted(declared_states - documented_states)}, "
            f"docs-only={sorted(documented_states - declared_states)}"
        )
    return failures


def corpus_failures(root: Path) -> list[str]:
    return (
        broken_internal_links(root)
        + missing_contract_fields(root)
        + unindexed_entries(root)
        + duplicate_local_titles(root)
        + case_contract_mismatches(root)
    )
