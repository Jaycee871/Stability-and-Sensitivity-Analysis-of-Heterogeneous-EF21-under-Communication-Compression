# Phase 8 — Submission-ready manuscript assembly

Phase 8 converts the audited research draft into a single free-format manuscript source suitable for MDPI pre-check while preserving explicit blockers that cannot be inferred safely.

## What is now automated

Running

```bash
python scripts/build_submission_package.py --paper-assets-dir paper_assets
```

produces a self-contained submission package with:

- `manuscript_free_format.md` — one continuous manuscript with numbered citations, embedded figure/table captions, Methods disclosure, and MDPI back matter;
- `references.bib` and a numbered reference list;
- figure captions;
- cover letter;
- editorial-independence note;
- submission metadata and checklist;
- full paper assets when `--paper-assets-dir` is supplied;
- `readiness_report.json` identifying unresolved final-submission blockers.

## Deliberately unresolved fields

The package is content-ready but must not be submitted until the following are supplied by the authors:

1. final author list and order;
2. affiliations;
3. corresponding author and email;
4. CRediT author contributions;
5. funding statement;
6. permanent public repository/OSF URL or DOI.

These appear as machine-detectable tokens rather than guessed values.

## Formatting decision

MDPI currently accepts both Word and LaTeX and also permits free-format initial submission when all required sections are present. The journal's 2026 article template was revised in December 2025. To avoid copying author/affiliation/archive metadata twice, this repository keeps Phase 8 in a complete free-format source and defers transfer into the current *Mathematics* house template until the six metadata blockers above are resolved.

## Claim discipline

Phase 8 changes presentation only. It does not alter formulas, numerical values, the audited 216,027-cell analysis, the off-grid robustness findings, or the fixed-stratum discriminant statement.
