# Phase 23c — MDPI Mathematics LaTeX integration

This directory stages the journal-template manuscript prepared from the official 2026 MDPI ACS LaTeX template supplied by the human author on 2026-08-11.

## Current authorship metadata

1. **Fu-Hsing Wang** — first author and corresponding author.
2. **Pack Kwan Low** — second author.

Shared affiliation staged in the manuscript:

> Department of Information Management, Chinese Culture University, 55 Hwa-Kang Rd., Yang-Ming-Shan, Taipei 11114, Taiwan.

Confirmed correspondence e-mail for Fu-Hsing Wang:

> `wang.fuhsing@gmail.com`

## Phase 23c display correction

The official MDPI class synthesizes a dummy footer DOI from the template volume/issue/article-number defaults even in submit mode. In the earlier author-facing PDF this appeared as `https://doi.org/10.3390/math1010000`. That string was a **template-generated placeholder, not an assigned DOI**.

Phase 23c adds a submit-mode footer guard to the LaTeX source so the author-facing draft no longer displays that placeholder. Existing DOI identifiers belonging to cited references remain unchanged.

## What is tracked here

The Phase 23b base `manuscript.tex` and `references.bib` remain stored as gzip-compressed Base64 payloads:

- `manuscript.tex.gz.b64`
- `references.bib.gz.b64`

Run:

```bash
python scripts/materialize_phase23_mdpi_latex.py
```

to reconstruct the exact Phase 23c editable sources under `submission/mdpi_latex/materialized/`. The materializer verifies the original payload hashes, applies the deterministic DOI-footer guard to `manuscript.tex`, and then verifies the final Phase 23c source hash.

The local Phase 23c package also contains the official MDPI `Definitions/` support files, publication Figures 1–8, Supplementary Figure S1, and the compiled 18-page PDF. Vendor/binary template assets and generated PDFs are intentionally not duplicated in Git history; publication figures remain reproducible from the repository paper-asset pipeline, and the current official MDPI template should be obtained from MDPI for final submission assembly.

## Local package integrity record

Phase 23c package:

`MDPI_Mathematics_EF21_LaTeX_Phase23c_NoPlaceholderDOI.zip`

SHA-256:

`3a9da65db0c9cfa8ef15c1712910dcad35b4494570a796ebd888095f03e06aa4`

Materialized Phase 23c `manuscript.tex` SHA-256:

`2ed375aa91d7b51b10f318eb03f587ea32bd776593ed4dfeac00dbee1a4ffeb3`

`references.bib` SHA-256:

`56d1eb6eb77845a3a5b9d85212aedd3687b59eb9105308bf7f199bacab9cb2a1`

## Scientific guardrail

The manuscript analyzes consequences of the inherited two-agent Empirical Law 4.3 cubic. It does **not** claim to prove Empirical Law 4.3 as a general EF21 convergence theorem.

## Still unresolved before submission

- ORCID identifiers;
- final CRediT contribution statement;
- funding statement;
- permanent public OSF URL/DOI after archive freeze;
- final Conflict of Interest wording after author review.
