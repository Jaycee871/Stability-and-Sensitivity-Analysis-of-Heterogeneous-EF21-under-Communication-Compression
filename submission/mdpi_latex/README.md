# Phase 23 — MDPI Mathematics LaTeX integration

This directory stages the journal-template manuscript prepared from the official 2026 MDPI ACS LaTeX template supplied by the human author on 2026-08-11.

## Current authorship metadata

1. **Fu-Hsing Wang** — first author and corresponding author.
2. **Pack Kwan Low** — second author.

Shared affiliation staged in the manuscript:

> Department of Information Management, Chinese Culture University, 55 Hwa-Kang Rd., Yang-Ming-Shan, Taipei 11114, Taiwan.

The preferred correspondence e-mail for Fu-Hsing Wang remains a submission-stage placeholder until confirmed.

## What is tracked here

The exact Phase 23b `manuscript.tex` and `references.bib` are stored as gzip-compressed Base64 payloads so that the journal source can be reproduced byte-for-byte without duplicating MDPI-owned binary template assets in the repository:

- `manuscript.tex.gz.b64`
- `references.bib.gz.b64`

Run:

```bash
python scripts/materialize_phase23_mdpi_latex.py
```

to reconstruct the two editable source files under `submission/mdpi_latex/materialized/`.

The compiled local Phase 23b package also contained the official MDPI `Definitions/` support files, publication figures 1–8, Supplementary Figure S1, and a compiled PDF. Those vendor/binary assets are intentionally not duplicated in Git history; the publication figures remain reproducible from the repository paper-asset pipeline, and the official current MDPI template should be obtained from MDPI for final submission assembly.

## Local package integrity record

The compiled package produced on 2026-08-11 had SHA-256:

`68eaf805f052b4fb557690b90d2d69d0dbdc0e3453e0e2830d6662f230db5a1d`

The staged `manuscript.tex` SHA-256 is:

`be4e9faa00cc48f05545d6da83df521778a14f748c83132cd9a552d16217706a`

The staged `references.bib` SHA-256 is:

`56d1eb6eb77845a3a5b9d85212aedd3687b59eb9105308bf7f199bacab9cb2a1`

## Scientific guardrail

The manuscript analyzes consequences of the inherited two-agent Empirical Law 4.3 cubic. It does **not** claim to prove Empirical Law 4.3 as a general EF21 convergence theorem.

## Still unresolved before submission

- Fu-Hsing Wang correspondence e-mail;
- ORCID identifiers;
- final CRediT contribution statement;
- funding statement;
- permanent public OSF URL/DOI after archive freeze;
- final Conflict of Interest wording after author review.
