# Phase 24 — MDPI Mathematics LaTeX integration

This directory stages the journal-template manuscript prepared from the official 2026 MDPI ACS LaTeX template supplied by the human author and subsequently reviewed in Overleaf.

## Current authorship metadata

1. **Pack Kwan Low** — first author.
2. **Fu-Hsing Wang** — second author and corresponding author.

Shared affiliation staged in the manuscript:

> Department of Information Management, Chinese Culture University, 55 Hwa-Kang Rd., Yang-Ming-Shan, Taipei 11114, Taiwan.

## Current reviewed title

**Stability and Sensitivity Analysis of Heterogeneous Error Feedback 21 (EF$^{21}$) under Communication Compression**

## Round 2 reviewed manuscript snapshot

The live Overleaf manuscript underwent substantive author/peer review after the earlier deterministic Phase 24 typography edits. Because those changes now include narrative restructuring, definition movement, a formal proposition, Discussion expansion, future-work text, theorem attribution, and PDF-metadata hygiene, the current reviewed manuscript is frozen as an integrity-checked compressed snapshot:

- `manuscript_phase24_round2.tex.gz.b64`

Materialize the current source with:

```bash
python scripts/materialize_phase24_mdpi_latex.py
```

The materializer still verifies the Phase 23c lineage before accepting the reviewed snapshot. The unchanged `references.bib` payload remains verified against the Phase 23c integrity record.

Current reviewed manuscript SHA-256:

`2ea4ead0e7c1164d3507fc5ab8aa6138ed2b82b63f1d781b4e8ba50b26fac40d`

## Round 2 review highlights

The current manuscript includes:

- direct first-use definitions of $q_i$, $w_i$, $K_1$, $K_2$, and $\operatorname{Var}_w(q_i)$;
- three consolidated contributions rather than six project-style bullets;
- early preview of the mismatch-coordinate collapse;
- positive contrastive positioning against nearby EF$^{21}$ heterogeneity work;
- **Proposition 1 (Conditional mismatch principle)** in Results;
- removal of internal labels such as `N1a`, `N1b`, `Phase 4`, and `Phase 13`;
- a Discussion paragraph on algebraic generalizability beyond two agents while keeping the cubic claims two-agent-specific;
- explicit attribution of the homogeneous baseline to Theorem 3.1 of Ref. [7];
- consistent use of $\rho_{\mathrm{hom}}$;
- PDF-string-safe `\texorpdfstring` fallbacks and LaTeX warning cleanup.

## Phase 23c display correction retained

The official MDPI class can synthesize a dummy footer DOI from template volume/issue/article-number defaults even in submit mode. Phase 23c added a submit-mode footer guard so the author-facing draft does not display that placeholder. Real DOI identifiers belonging to cited references remain unchanged.

## Scientific guardrail

The manuscript analyzes consequences of the reproduced two-agent Empirical Law 4.3 cubic. It does **not** claim to prove Empirical Law 4.3 as a general EF$^{21}$ convergence theorem. The weighted-moment variance identity is algebraically broader, but the fixed-average factorization and root-sensitivity results remain scoped to the inherited two-agent cubic.

## Still unresolved before submission

- final ORCID/author metadata confirmation as applicable;
- final CRediT contribution statement;
- funding statement;
- permanent public OSF URL/DOI after archive freeze;
- final Conflict of Interest wording after author review;
- final figure/layout consolidation and submission-package freeze.
