# Phase 23 — MDPI Mathematics LaTeX integration

## Purpose

Phase 23 moves the Phase 20 manuscript from MDPI-compatible free format into the official 2026 MDPI ACS LaTeX house template for *Mathematics* while preserving the Phase 17–22 claim and reproducibility guardrails.

## Staged author metadata

- **Fu-Hsing Wang** — first author and corresponding author.
- **Pack Kwan Low** — second author.
- Shared affiliation: Department of Information Management, Chinese Culture University, 55 Hwa-Kang Rd., Yang-Ming-Shan, Taipei 11114, Taiwan.
- Fu-Hsing Wang's preferred correspondence e-mail remains unresolved and is intentionally left as a placeholder.

## LaTeX conversion state

The local Phase 23b package was produced from the official MDPI ACS template supplied by the human author. The package compiled successfully to an 18-page PDF in the staging environment.

The journal-formatted manuscript integrates:

- the equal-smoothness reproduction and 216,027-cell controlled baseline;
- the full-regularity fixed-average extension;
- the inherited weighted-moment reinterpretation of `K1-K2`;
- the explicit `(tau_L-tau_mu)^2` mismatch factorization;
- aligned-heterogeneity invariance;
- the generic inherited-cubic root-location and sensitivity result;
- Figures 1–8 and Supplementary Figure S1;
- the AI-assisted research-workflow disclosure;
- the current data-availability and conflict-of-interest staging statements.

## Exact source preservation

To keep the repository reviewable without duplicating MDPI-owned binary template assets, the exact Phase 23b `manuscript.tex` and `references.bib` are stored as gzip-compressed Base64 payloads under `submission/mdpi_latex/`. `scripts/materialize_phase23_mdpi_latex.py` reconstructs them and verifies their SHA-256 digests.

Local package SHA-256:

`68eaf805f052b4fb557690b90d2d69d0dbdc0e3453e0e2830d6662f230db5a1d`

## Scientific guardrails retained

1. Empirical Law 4.3 remains an inherited empirical object, not a proved general EF21 convergence theorem.
2. `K1-K2 = Var_w(q_i)` remains an inherited algebraic reinterpretation; no standalone novelty claim is attached to the identity itself.
3. The fixed-average factorization, aligned-path consequence, and inherited-cubic sensitivity are stated as scoped analyses.
4. Full-regularity structural conclusions remain restricted to the inherited two-agent cubic.
5. The named literature chain is closed for the audited references, but universal novelty is not certified.

## Remaining submission blockers

- corresponding-author e-mail;
- ORCID identifiers;
- final CRediT statement;
- funding statement;
- permanent public OSF URL/DOI after archival freeze;
- final author-reviewed conflict-of-interest wording;
- final technical compilation using the then-current official MDPI template.
