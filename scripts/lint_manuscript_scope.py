#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATTERNS = {
    "prove_empirical_law": r"\b(?:we\s+)?prove(?:s|d)?\s+(?:the\s+)?Empirical\s+Law\s+4\.3\b",
    "general_ef21_theorem": r"\bwe\s+(?:prove|establish|derive)\s+(?:a\s+)?general\s+EF21\s+(?:convergence\s+)?theorem\b",
    "universal_stability_threshold": r"\b(?:is|are|gives?|yields?)\s+(?:a\s+)?universal\s+stability\s+thresholds?\b",
    "global_monotonicity_claim": r"\b(?:we\s+)?prove(?:s|d)?\s+global\s+monotonicity\b",
    "arbitrary_n_claim": r"\b(?:for|across)\s+arbitrary\s+(?:n|numbers?\s+of\s+workers?)\b",
}

REQUIRED_GUARDRAILS = [
    "does not attempt to prove the full heterogeneous empirical law",
    "not universal convergence thresholds",
    "not proofs of global monotonicity",
    "only for the three fixed conditioning strata",
    "not a direct communication-cost optimum",
]


def lint(text: str) -> dict[str, object]:
    violations = []
    for name, pattern in FORBIDDEN_PATTERNS.items():
        matches = [m.group(0) for m in re.finditer(pattern, text, flags=re.I)]
        if matches:
            violations.append({"rule": name, "matches": matches})

    lower = text.lower()
    missing_guardrails = [phrase for phrase in REQUIRED_GUARDRAILS if phrase.lower() not in lower]

    return {
        "forbidden_pattern_violations": violations,
        "missing_required_guardrails": missing_guardrails,
        "pass": not violations and not missing_guardrails,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manuscript", type=Path, default=Path("manuscript/draft.md"))
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    path = args.manuscript if args.manuscript.is_absolute() else ROOT / args.manuscript
    report = lint(path.read_text(encoding="utf-8"))
    if args.output is not None:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
