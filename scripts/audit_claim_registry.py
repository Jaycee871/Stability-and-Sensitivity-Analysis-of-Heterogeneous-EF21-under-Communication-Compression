#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def get_path(value: Any, dotted: str) -> Any:
    current = value
    for part in dotted.split("."):
        if isinstance(current, list):
            current = current[int(part)]
        elif isinstance(current, dict):
            current = current[part]
        else:
            raise TypeError(f"cannot descend into {type(current).__name__} at {part}")
    return current


def evidence_check(item: dict[str, Any]) -> tuple[bool, str, Any]:
    source = ROOT / item["source"]
    if not source.exists():
        return False, f"missing source {item['source']}", None

    if source.suffix.lower() == ".json":
        payload = json.loads(source.read_text(encoding="utf-8"))
        actual = get_path(payload, item["path"])
    else:
        actual = source.read_text(encoding="utf-8")

    if "expected_contains" in item:
        expected = str(item["expected_contains"])
        ok = expected in str(actual)
        return ok, f"contains {expected!r}", actual

    expected = item["expected"]
    if isinstance(expected, bool):
        ok = actual is expected
    elif isinstance(expected, (int, float)) and not isinstance(expected, bool):
        tolerance = float(item.get("tolerance", 0.0))
        ok = math.isclose(float(actual), float(expected), rel_tol=0.0, abs_tol=tolerance)
    else:
        ok = actual == expected
    return ok, f"expected {expected!r}", actual


def audit(registry_path: Path) -> dict[str, Any]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    manuscript = (ROOT / registry["manuscript"]).read_text(encoding="utf-8")

    rows: list[dict[str, Any]] = []
    all_pass = True
    for claim in registry["claims"]:
        manuscript_ok = claim["manuscript_match"] in manuscript
        evidence_rows = []
        evidence_ok = True
        for item in claim["evidence"]:
            ok, expectation, actual = evidence_check(item)
            evidence_ok = evidence_ok and ok
            evidence_rows.append(
                {
                    "source": item["source"],
                    "path": item.get("path"),
                    "ok": ok,
                    "expectation": expectation,
                    "actual": actual,
                }
            )
        claim_ok = manuscript_ok and evidence_ok
        all_pass = all_pass and claim_ok
        rows.append(
            {
                "id": claim["id"],
                "short_claim": claim["short_claim"],
                "evidence_level": claim["evidence_level"],
                "manuscript_match": claim["manuscript_match"],
                "manuscript_ok": manuscript_ok,
                "evidence_ok": evidence_ok,
                "claim_ok": claim_ok,
                "guardrail": claim["guardrail"],
                "evidence": evidence_rows,
            }
        )

    return {
        "registry_version": registry["version"],
        "claims_total": len(rows),
        "claims_passed": sum(int(row["claim_ok"]) for row in rows),
        "all_claims_verified": all_pass,
        "claims": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Claim-to-Evidence Matrix",
        "",
        f"Verified claims: **{report['claims_passed']}/{report['claims_total']}**",
        "",
        "This audit links manuscript-level claims to version-controlled evidence. It does not upgrade computational observations into theorems; each row retains its scope guardrail.",
        "",
        "| ID | Evidence level | Claim | Evidence | Guardrail |",
        "|---|---|---|---|---|",
    ]
    for row in report["claims"]:
        evidence = "; ".join(
            f"`{item['source']}`" + (f" → `{item['path']}`" if item["path"] else "")
            for item in row["evidence"]
        )
        status = "PASS" if row["claim_ok"] else "FAIL"
        lines.append(
            f"| {row['id']} {status} | {row['evidence_level']} | {row['short_claim']} | {evidence} | {row['guardrail']} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation hierarchy",
            "",
            "- **Inherited-literature** claims reproduce or parameterize statements from the cited source paper and must retain the original empirical/theoretical status.",
            "- **Computational** claims are tied to audited finite grids, bisection procedures, or deterministic off-grid stress tests.",
            "- **Analytic-symbolic** claims follow from exact symbolic factorization for the explicitly tested fixed-conditioning strata.",
            "- No row in this registry is permission to claim a general proof of Empirical Law 4.3 or a method-agnostic communication-complexity theorem.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=Path("claims/claim_registry.json"))
    parser.add_argument("--output-json", type=Path, default=Path("results/phase9_claim_audit.json"))
    parser.add_argument("--output-md", type=Path, default=Path("docs/claim_evidence_matrix.md"))
    args = parser.parse_args()

    registry_path = args.registry if args.registry.is_absolute() else ROOT / args.registry
    report = audit(registry_path)

    json_path = args.output_json if args.output_json.is_absolute() else ROOT / args.output_json
    md_path = args.output_md if args.output_md.is_absolute() else ROOT / args.output_md
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")

    print(json.dumps({
        "claims_total": report["claims_total"],
        "claims_passed": report["claims_passed"],
        "all_claims_verified": report["all_claims_verified"],
    }, indent=2))
    if not report["all_claims_verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
