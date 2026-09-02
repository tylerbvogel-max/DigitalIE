"""Small dependency-free integrity rules used by fixtures and future adapters."""


def verified_hypothesis_is_defensible(hypothesis: dict, evidence_ids: set[str]) -> bool:
    """A verified causal claim needs linked evidence, validation, and approval."""
    if hypothesis.get("status") != "verified":
        return True
    return bool(
        hypothesis.get("evidence_ids")
        and set(hypothesis["evidence_ids"]).issubset(evidence_ids)
        and hypothesis.get("validation_test_id")
        and hypothesis.get("approved_by")
    )
