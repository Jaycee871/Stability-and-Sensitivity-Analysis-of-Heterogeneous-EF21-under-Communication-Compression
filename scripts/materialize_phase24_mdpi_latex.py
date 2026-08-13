#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from materialize_phase23_mdpi_latex import (
    BASE_FILES,
    FINAL_SHA256 as PHASE23C_FINAL_SHA256,
    SOURCE_DIR,
    decode_payload,
    phase23c_manuscript,
    sha256,
)

ROUND2_MANUSCRIPT_PAYLOAD = SOURCE_DIR / "manuscript_phase24_round2.tex.gz.b64"
ROUND2_MANUSCRIPT_SHA256 = "2ea4ead0e7c1164d3507fc5ab8aa6138ed2b82b63f1d781b4e8ba50b26fac40d"


def validate_round2_manuscript(data: bytes) -> None:
    text = data.decode("utf-8")

    required = [
        "Pack Kwan Low $^{1}$ and Fu-Hsing Wang $^{1,}$*",
        "Error Feedback 21\n(\\texorpdfstring{EF$^{21}$}{EF21}) under Communication Compression",
        "\\emph{Statistical or data heterogeneity}",
        "\\emph{Regularity heterogeneity}",
        "\\emph{local condition-shape coordinate}",
        "K_1=\\sum_{i=1}^{2} w_iq_i^2",
        "\\operatorname{Var}_w(q_i)\n:=",
        "The study makes three main contributions.",
        "the apparent two-dimensional heterogeneity dependence collapses onto a single nonnegative mismatch coordinate",
        "\\begin{Proposition}[Conditional mismatch principle]",
        "Algebraic generalizability beyond two agents",
        "Theorem 3.1 of Ref.~\\citep{thomsen2026tight}",
        "\\subsection{Relation to prior \\texorpdfstring{EF$^{21}$}{EF21} heterogeneity analyses}",
        "\\setlength{\\headheight}{19pt}",
        "Future work should test whether analogous mismatch coordinates emerge for $n>2$",
        "{\\nolinkurl{doi:10.48550/arXiv.2402.10774}}",
    ]
    for marker in required:
        if marker not in text:
            raise SystemExit(f"Phase 24 Round 2 validation marker missing: {marker}")

    forbidden = [
        "N1a",
        "N1b",
        "Phase 4",
        "Phase 13",
        "\\rho_{\\rm homogeneous}",
        "their difference will later be shown",
    ]
    for marker in forbidden:
        if marker in text:
            raise SystemExit(f"Phase 24 Round 2 forbidden legacy marker found: {marker}")

    if text.count("\\begin{Proposition}[Conditional mismatch principle]") != 1:
        raise SystemExit("Phase 24 Round 2 proposition count is not exactly one")

    q_pos = text.index("q_i=\n\\frac{\\Delta_i}{\\Sigma_i}")
    k_pos = text.index("K_1=\\sum_{i=1}^{2} w_iq_i^2")
    if q_pos >= k_pos:
        raise SystemExit("Phase 24 Round 2 K1/K2 definitions appear before q_i")

    results_pos = text.index("\\section{Results}")
    proposition_pos = text.index("\\begin{Proposition}[Conditional mismatch principle]")
    discussion_pos = text.index("\\section{Discussion}")
    if not (results_pos < proposition_pos < discussion_pos):
        raise SystemExit("Phase 24 Round 2 proposition is not located in Results")

    if "EF21: A new, simpler, theoretically better, and practically faster error feedback." not in text:
        raise SystemExit("Phase 24 bibliography guard failed: formal EF21 title was altered")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct the Phase 24 MDPI source after live author/peer review. "
            "The reviewed manuscript is stored as an integrity-checked compressed "
            "snapshot while the unchanged reference payload remains traced to Phase 23c."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=SOURCE_DIR / "materialized_phase24",
    )
    args = parser.parse_args()

    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Preserve the Phase 23c lineage check before accepting the reviewed snapshot.
    base_manuscript_spec = BASE_FILES["manuscript.tex"]
    base_manuscript = decode_payload(SOURCE_DIR / base_manuscript_spec["payload"])
    if sha256(base_manuscript) != base_manuscript_spec["base_sha256"]:
        raise SystemExit("Phase 23b base manuscript integrity failure")
    phase23c = phase23c_manuscript(base_manuscript)
    if sha256(phase23c) != PHASE23C_FINAL_SHA256["manuscript.tex"]:
        raise SystemExit("Phase 23c manuscript lineage integrity failure")

    manuscript = decode_payload(ROUND2_MANUSCRIPT_PAYLOAD)
    digest = sha256(manuscript)
    if digest != ROUND2_MANUSCRIPT_SHA256:
        raise SystemExit(
            "Phase 24 Round 2 snapshot integrity failure: "
            f"expected {ROUND2_MANUSCRIPT_SHA256}, got {digest}"
        )
    validate_round2_manuscript(manuscript)
    target = out / "manuscript.tex"
    target.write_bytes(manuscript)
    print(f"materialized {target} sha256={digest}")

    # references.bib remains the verified Phase 23c reference payload.
    ref_spec = BASE_FILES["references.bib"]
    references = decode_payload(SOURCE_DIR / ref_spec["payload"])
    if sha256(references) != ref_spec["base_sha256"]:
        raise SystemExit("references.bib base integrity failure")
    if sha256(references) != PHASE23C_FINAL_SHA256["references.bib"]:
        raise SystemExit("references.bib Phase 23c integrity failure")
    ref_target = out / "references.bib"
    ref_target.write_bytes(references)
    print(f"materialized {ref_target} sha256={sha256(references)}")

    print(
        "Phase 24 Round 2 author-review snapshot validated: first-use definitions, "
        "three-contribution narrative, conditional proposition, n>2 algebraic "
        "discussion, theorem attribution, PDF-string-safe EF^{21} metadata, "
        "symbol consistency, and bibliographic guards are present."
    )


if __name__ == "__main__":
    main()
