# Phase 24 — MDPI Mathematics LaTeX integration

This directory stages the journal-template manuscript prepared from the official 2026 MDPI ACS LaTeX template supplied by the human author on 2026-08-11.

## Current authorship metadata

1. **Pack Kwan Low** — first author.
2. **Fu-Hsing Wang** — second author and corresponding author.

Shared affiliation staged in the manuscript:

> Department of Information Management, Chinese Culture University, 55 Hwa-Kang Rd., Yang-Ming-Shan, Taipei 11114, Taiwan.

The corresponding-author role remains with Fu-Hsing Wang.

## Phase 24 author-review correction

Author review revised the manuscript order so the author with the largest contribution is listed first. Phase 24 therefore changes the displayed and running author order from `Fu-Hsing Wang; Pack Kwan Low` to `Pack Kwan Low; Fu-Hsing Wang`, while preserving Fu-Hsing Wang as corresponding author.

The scientific text, scope guardrails, figures, references, and DOI-footer correction are unchanged by this authorship-only transform.

## Phase 23c display correction retained

The official MDPI class synthesizes a dummy footer DOI from the template volume/issue/article-number defaults even in submit mode. In the earlier author-facing PDF this appeared as `https://doi.org/10.3390/math1010000`. That string was a **template-generated placeholder, not an assigned DOI**.

Phase 23c added a submit-mode footer guard so the author-facing draft no longer displays that placeholder. Existing DOI identifiers belonging to cited references remain unchanged.

## What is tracked here

The Phase 23b base `manuscript.tex` and `references.bib` remain stored as gzip-compressed Base64 payloads:

- `manuscript.tex.gz.b64`
- `references.bib.gz.b64`

Phase 23c reconstruction remains available through:

```bash
python scripts/materialize_phase23_mdpi_latex.py
```

For the current Phase 24 author-reviewed manuscript, run:

```bash
python scripts/materialize_phase24_mdpi_latex.py
```

The Phase 24 materializer first verifies and reconstructs the exact Phase 23c source, then applies only the deterministic author-order correction. The corresponding-author line remains Fu-Hsing Wang.

The local submission package additionally requires the official MDPI `Definitions/` support files, publication Figures 1–8, Supplementary Figure S1, and the compiled PDF. Vendor/binary template assets and generated PDFs are intentionally not duplicated in Git history; publication figures remain reproducible from the repository paper-asset pipeline, and the current official MDPI template should be obtained from MDPI for final submission assembly.

## Phase 23c integrity record retained

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

- final ORCID/author metadata confirmation as applicable;
- final CRediT contribution statement;
- funding statement;
- permanent public OSF URL/DOI after archive freeze;
- final Conflict of Interest wording after author review.
