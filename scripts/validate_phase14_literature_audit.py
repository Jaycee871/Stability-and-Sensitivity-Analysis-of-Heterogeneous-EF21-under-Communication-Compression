#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PENDING = "PENDING_EXTERNAL_AUDIT"
FINAL_STATUSES = {
    "CLEAR_TO_PROMOTE",
    "PROMOTE_WITH_PRIOR_ART_POSITIONING",
    "REQUIRES_MANUAL_EQUIVALENCE_CHECK",
    "NOVELTY_CLAIM_MUST_BE_NARROWED",
    "DO_NOT_CLAIM_NOVELTY",
}
CLASSIFICATIONS = {"A", "B", "C", "D"}


def validate(payload: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []

    if payload.get("phase") != 14:
        errors.append("phase must equal 14")

    claims = payload.get("claims")
    if not isinstance(claims, dict) or set(claims) != {"N1", "N2", "N3", "N4"}:
        errors.append("claims must contain exactly N1, N2, N3, N4")
        claims = claims if isinstance(claims, dict) else {}

    required_fields = payload.get("required_candidate_fields", [])
    if not isinstance(required_fields, list) or not required_fields:
        errors.append("required_candidate_fields must be a non-empty list")
        required_fields = []

    candidates = payload.get("candidates", [])
    if not isinstance(candidates, list):
        errors.append("candidates must be a list")
        candidates = []

    ids: set[str] = set()
    candidate_map: dict[str, dict[str, Any]] = {}
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            errors.append(f"candidate[{index}] must be an object")
            continue
        missing = [field for field in required_fields if field not in candidate]
        if missing:
            errors.append(f"candidate[{index}] missing fields: {', '.join(missing)}")
        candidate_id = str(candidate.get("candidate_id", "")).strip()
        if not candidate_id:
            errors.append(f"candidate[{index}] has empty candidate_id")
        elif candidate_id in ids:
            errors.append(f"duplicate candidate_id: {candidate_id}")
        else:
            ids.add(candidate_id)
            candidate_map[candidate_id] = candidate
        classification = candidate.get("classification")
        if classification not in CLASSIFICATIONS:
            errors.append(
                f"candidate[{index}] classification must be one of {sorted(CLASSIFICATIONS)}"
            )
        if candidate.get("manual_source_checked") not in {True, False}:
            errors.append(f"candidate[{index}] manual_source_checked must be boolean")

    external_pending = payload.get("status") == PENDING
    for claim_id in ("N1", "N2", "N3", "N4"):
        claim = claims.get(claim_id, {}) if isinstance(claims, dict) else {}
        status = claim.get("status")
        strongest = claim.get("strongest_candidate_id")
        manual = claim.get("manual_equivalence_verified")

        if external_pending:
            if status != PENDING:
                errors.append(
                    f"{claim_id} must remain {PENDING} while overall audit is pending"
                )
            if strongest is not None:
                errors.append(
                    f"{claim_id} strongest_candidate_id must remain null before external audit"
                )
            if manual is not False:
                errors.append(
                    f"{claim_id} manual_equivalence_verified must remain false before external audit"
                )
            continue

        if status not in FINAL_STATUSES:
            errors.append(f"{claim_id} has invalid post-audit status: {status!r}")
        if strongest is not None and strongest not in candidate_map:
            errors.append(
                f"{claim_id} strongest_candidate_id {strongest!r} is not in candidates"
            )

        # Any direct/material-overlap candidate used to adjudicate a claim must
        # have been manually checked in the original source before promotion.
        if status in {"CLEAR_TO_PROMOTE", "PROMOTE_WITH_PRIOR_ART_POSITIONING"}:
            unchecked_ab = [
                cid
                for cid, candidate in candidate_map.items()
                if candidate.get("classification") in {"A", "B"}
                and not candidate.get("manual_source_checked")
            ]
            if unchecked_ab:
                errors.append(
                    f"{claim_id} cannot be promoted while A/B candidates remain unchecked: "
                    + ", ".join(sorted(unchecked_ab))
                )

    return {
        "phase": 14,
        "status": payload.get("status"),
        "candidate_count": len(candidates),
        "valid": not errors,
        "errors": errors,
        "interpretation": (
            "A valid pending matrix means only that the novelty audit is correctly "
            "blocked awaiting external search; it is not evidence that any claim is novel."
            if external_pending
            else "A valid completed matrix means the required schema/guardrails are satisfied; scientific novelty still depends on the recorded source adjudication."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("literature/phase14_candidate_matrix.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("results/phase14_literature_audit_validation.json"),
    )
    args = parser.parse_args()

    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    output_path = args.output if args.output.is_absolute() else ROOT / args.output

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    report = validate(payload)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
