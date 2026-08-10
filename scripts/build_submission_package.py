#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# MDPI free-format numbering follows first appearance in the Phase 20 manuscript.
CITATION_NUMBERS = {
    "thomsen2026tight": 1,
    "seide2014onebit": 2,
    "stich2018sparsified": 3,
    "karimireddy2019error": 4,
    "richtarik2021ef21": 5,
    "richtarik2024reloaded": 6,
    "gao2023econtrol": 7,
    "drori2014performance": 8,
    "taylor2017exact": 9,
    "colla2024symmetries": 10,
}

BLOCKERS = {
    "[AUTHOR LIST REQUIRED BEFORE SUBMISSION]": "final author list and order",
    "[AFFILIATIONS REQUIRED BEFORE SUBMISSION]": "final affiliations",
    "[CORRESPONDING AUTHOR REQUIRED BEFORE SUBMISSION]": "corresponding author and email",
    "[AUTHOR CONTRIBUTIONS REQUIRED BEFORE SUBMISSION]": "CRediT author contributions",
    "[FUNDING STATEMENT REQUIRED BEFORE SUBMISSION]": "funding statement",
    "[PUBLIC ARCHIVE URL/DOI REQUIRED BEFORE SUBMISSION]": "public OSF/repository URL or DOI",
}


def replace_citations(text: str) -> str:
    pattern = re.compile(r"\[(?=[^\]]*@)([^\]]+)\]")

    def repl(match: re.Match[str]) -> str:
        keys = re.findall(r"@([A-Za-z0-9_:-]+)", match.group(1))
        if not keys:
            return match.group(0)
        missing = [key for key in keys if key not in CITATION_NUMBERS]
        if missing:
            raise ValueError(f"unmapped citation keys: {missing}")
        numbers = [str(CITATION_NUMBERS[key]) for key in keys]
        return "[" + ",".join(numbers) + "]"

    return pattern.sub(repl, text)


def extract_draft_body(text: str) -> tuple[str, str]:
    abstract_match = re.search(r"## Abstract\n\n(.*?)\n\n## 1\. Introduction", text, re.S)
    if not abstract_match:
        raise ValueError("draft abstract could not be located")
    abstract = abstract_match.group(1).strip()
    body = text[text.index("## 1. Introduction") :]
    body = re.split(r"\n## Figure and table map\n", body, maxsplit=1)[0].rstrip()
    body = re.split(r"\n## References\n", body, maxsplit=1)[0].rstrip()
    return abstract, body


def parse_captions(text: str) -> dict[str, str]:
    captions: dict[str, str] = {}
    chunks = re.split(r"\n## ", "\n" + text)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk or chunk.startswith("# Figure captions"):
            continue
        heading, _, body = chunk.partition("\n\n")
        for label in (
            "Figure 1",
            "Figure 2",
            "Figure 3",
            "Figure 4",
            "Figure 5",
            "Figure 6",
            "Figure 7",
            "Figure 8",
            "Figure S1",
            "Table 1",
        ):
            if heading.startswith(label):
                captions[label] = body.strip()
                break

    required = {
        "Figure 1",
        "Figure 2",
        "Figure 3",
        "Figure 4",
        "Figure 5",
        "Figure 6",
        "Figure 7",
        "Figure 8",
        "Figure S1",
        "Table 1",
    }
    missing = required - captions.keys()
    if missing:
        raise ValueError(f"missing captions: {sorted(missing)}")
    return captions


def insert_figure_captions(body: str, captions: dict[str, str]) -> str:
    replacements = {
        "**Figure file:** `paper_assets/figures/figure1_contraction_landscape.svg`":
            "**[Insert Figure 1 here]**\n\n" + captions["Figure 1"],
        "**Figure file:** `paper_assets/figures/figure2_normalized_penalty.svg`":
            "**[Insert Figure 2 here]**\n\n" + captions["Figure 2"],
        "**Figure file:** `paper_assets/figures/figure3_conditioning_interaction.svg`":
            "**[Insert Figure 3 here]**\n\n" + captions["Figure 3"],
        "**Figure file:** `paper_assets/figures/figure4_retention_boundary.svg`":
            "**[Insert Figure 4 here]**\n\n" + captions["Figure 4"],
        "**Figure file:** `paper_assets/figures/figure5_boundary_convergence.svg`":
            "**[Insert Figure 5 here]**\n\n" + captions["Figure 5"],
        "**Figure file:** `paper_assets/phase19_full_regularity/figure6_mismatch_geometry.svg`":
            "**[Insert Figure 6 here]**\n\n" + captions["Figure 6"],
        "**Figure file:** `paper_assets/phase19_full_regularity/figure7_full_regularity_penalty.svg`":
            "**[Insert Figure 7 here]**\n\n" + captions["Figure 7"],
        "**Figure file:** `paper_assets/phase19_full_regularity/figure8_rate_collapse.svg`":
            "**[Insert Figure 8 here]**\n\n" + captions["Figure 8"],
        "**Supplementary figure:** `paper_assets/figures/figureS1_symbolic_root_structure.svg`":
            "**[Insert Figure S1 in Supplementary Materials]**\n\n" + captions["Figure S1"],
    }
    for old, new in replacements.items():
        if old not in body:
            raise ValueError(f"expected figure marker missing: {old}")
        body = body.replace(old, new)

    table_block = (
        "\n\n**[Insert Table 1 here]**\n\n"
        + captions["Table 1"]
        + "\n\nTable file: `tables/table1_key_results.csv`."
    )
    body = body.replace("\n## 5. Discussion", table_block + "\n\n## 5. Discussion", 1)
    return body


def build_manuscript() -> str:
    draft = (ROOT / "manuscript" / "draft.md").read_text(encoding="utf-8")
    captions_text = (ROOT / "manuscript" / "figure_captions.md").read_text(encoding="utf-8")
    references = (ROOT / "manuscript" / "reference_list.md").read_text(encoding="utf-8")
    abstract, body = extract_draft_body(draft)
    abstract = replace_citations(abstract)
    captions = parse_captions(captions_text)
    body = insert_figure_captions(body, captions)

    methods_disclosure = (
        "### 3.9 AI-assisted research workflow\n\n"
        "Generative AI was used as a research-assistance layer during study design, software development, "
        "verification planning, literature-audit organization, and manuscript preparation. ChatGPT (OpenAI; GPT-5.6 Sol) assisted in drafting "
        "and reviewing analysis code, structuring computational validation, and preparing manuscript text. "
        "Numerical conclusions were generated by version-controlled Python code and regression-tested in GitHub "
        "Actions. Symbolic claims were independently evaluated with Wolfram Language 15.0.1 and were not accepted "
        "solely on the basis of language-model output. Cross-model literature-search outputs were treated as candidate evidence and were manually checked against primary sources before affecting claim scope. All outputs were reviewed by the human authors.\n\n"
    )
    body = body.replace("## 4. Results", methods_disclosure + "## 4. Results", 1)
    body = replace_citations(body)

    front = f"""# Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression

**Article type:** Article  
**Journal:** *Mathematics* (MDPI)  
**Special Issue:** Artificial Intelligence and Algorithms  
**Authors:** [AUTHOR LIST REQUIRED BEFORE SUBMISSION]  
**Affiliations:** [AFFILIATIONS REQUIRED BEFORE SUBMISSION]  
**Corresponding author:** [CORRESPONDING AUTHOR REQUIRED BEFORE SUBMISSION]

## Abstract

{abstract}

**Keywords:** distributed optimization; error feedback; EF21; communication compression; heterogeneous optimization; convergence rate; stability analysis; sensitivity analysis

"""

    back = """

## Author Contributions

[AUTHOR CONTRIBUTIONS REQUIRED BEFORE SUBMISSION]

## Funding

[FUNDING STATEMENT REQUIRED BEFORE SUBMISSION]

## Institutional Review Board Statement

Not applicable. This study does not involve human participants or animals.

## Informed Consent Statement

Not applicable.

## Data Availability Statement

The complete computational workflow, generated numerical outputs, analysis scripts, literature-audit records, and figure-building code will be archived in a publicly accessible repository before final submission. Permanent archive identifier: [PUBLIC ARCHIVE URL/DOI REQUIRED BEFORE SUBMISSION].

## Acknowledgments

During the preparation of this study and manuscript, the authors used ChatGPT (OpenAI; GPT-5.6 Sol) to assist with research-workflow design, code generation and review, computational experiment planning, interpretation checks, literature-audit organization, and manuscript drafting/editing. Wolfram Language 15.0.1 was used as an independent symbolic computation engine for algebraic simplification, discriminant analysis, root-location checks, and sensitivity verification. All AI-assisted outputs, code, numerical results, symbolic results, citations, and manuscript text were reviewed and verified by the human authors, who take full responsibility for the content of the publication.

## Conflicts of Interest

The authors declare no financial conflict of interest. The Special Issue Guest Editor, Prof. Dr. Fuhsing Wang, is the academic advisor of the submitting author; independent editorial handling is requested to avoid any actual or perceived editorial conflict. This wording must be revised if the Guest Editor is included as a co-author.

## References

"""
    numbered_refs = references.split("Citation-number map used", 1)[0].replace(
        "# Numbered reference list for MDPI free-format submission\n\n", ""
    ).strip()
    return front + body + back + numbered_refs + "\n"


def count_words(text: str) -> int:
    cleaned = re.sub(r"`[^`]*`", " ", text)
    cleaned = re.sub(r"\[[^\]]*\]", " ", cleaned)
    return len(re.findall(r"\b[\w’'-]+\b", cleaned, flags=re.UNICODE))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("submission_package"))
    parser.add_argument("--paper-assets-dir", type=Path, default=None)
    args = parser.parse_args()

    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    manuscript = build_manuscript()
    (out / "manuscript_free_format.md").write_text(manuscript, encoding="utf-8")

    copies = {
        ROOT / "manuscript" / "references.bib": out / "references.bib",
        ROOT / "manuscript" / "figure_captions.md": out / "figure_captions.md",
        ROOT / "submission" / "cover_letter.md": out / "cover_letter.md",
        ROOT / "submission" / "editorial_independence_note.md": out / "editorial_independence_note.md",
        ROOT / "submission" / "submission_metadata.md": out / "submission_metadata.md",
        ROOT / "submission" / "checklist.md": out / "submission_checklist.md",
    }
    for src, dst in copies.items():
        shutil.copy2(src, dst)

    if args.paper_assets_dir is not None:
        if not args.paper_assets_dir.exists():
            raise FileNotFoundError(args.paper_assets_dir)
        shutil.copytree(args.paper_assets_dir, out / "paper_assets", dirs_exist_ok=True)

    unresolved = [
        {"token": token, "required_action": action}
        for token, action in BLOCKERS.items()
        if token in manuscript
    ]
    report = {
        "phase": 20,
        "target": "MDPI Mathematics / Artificial Intelligence and Algorithms",
        "format": "MDPI-compatible free-format submission source",
        "content_ready": True,
        "final_submission_ready": len(unresolved) == 0,
        "word_count_approx": count_words(manuscript),
        "citations_resolved_to_numbered_references": "[@" not in manuscript,
        "figures_integrated": [1, 2, 3, 4, 5, 6, 7, 8, "S1"],
        "required_sections_present": all(
            heading in manuscript
            for heading in [
                "## Abstract",
                "## 1. Introduction",
                "## 3. Methods",
                "## 4. Results",
                "## 5. Discussion",
                "## 6. Limitations",
                "## 7. Conclusion",
                "## Author Contributions",
                "## Funding",
                "## Data Availability Statement",
                "## Acknowledgments",
                "## Conflicts of Interest",
                "## References",
            ]
        ),
        "unresolved_submission_blockers": unresolved,
        "notes": [
            "MDPI accepts free-format manuscripts provided required sections are present.",
            "Transfer to the current Mathematics Word/LaTeX house template should occur after author metadata and archive identifiers are finalized.",
            "Phase 20 integrates the full-regularity Figure 6-8 visual evidence into the manuscript and submission-package pipeline while preserving the empirical-law scope guardrail.",
        ],
    }
    (out / "readiness_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
