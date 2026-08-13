# Phase 24 author review log

## 2026-08-11 — Authorship order

Author review established the current manuscript order as:

1. **Pack Kwan Low** — first author.
2. **Fu-Hsing Wang** — second author and corresponding author.

The authorship correction changes front matter and submission metadata only. It does not modify the scientific claims, numerical results, symbolic analysis, figures, references, or the manuscript's two-agent / Empirical Law 4.3 scope guardrails.

## 2026-08-11 — EF$^{21}$ notation and first-use expansion

Author review requested the algorithm name be typeset as `EF$^{21}$` rather than plain `EF21`. Follow-up clarification established the first visible wording as **Error Feedback 21 (EF$^{21}$)**. Bibliographic titles remain verbatim, including the published NeurIPS title beginning with plain `EF21`.

## 2026-08-12 — First-use technical-term emphasis

Author review requested that defined/distinguished technical terms be italicized at first manuscript occurrence. The implementation remains conservative: proper names, algorithm names, theorem/law labels, acronyms, and formal bibliographic titles keep standard typography.

## 2026-08-12 — $K_1$ / $K_2$ first-definition closure

Author review asked what the inherited coefficients $K_1$ and $K_2$ represent and then clarified that the explanation must occur **at first definition**, not later in Methods.

The Background now defines, in order:

- $\Sigma_i=L_i+\mu_i$ and $\Delta_i=L_i-\mu_i$;
- the local condition-shape coordinate $q_i=\Delta_i/\Sigma_i$;
- normalized weights $w_i=\Sigma_i/(\Sigma_1+\Sigma_2)$;
- $K_1$ as the weighted second moment and $K_2$ as the squared weighted mean;
- $K_1-K_2=\operatorname{Var}_w(q_i)$ with the weighted variance defined explicitly;
- the algebraically equivalent inherited two-agent closed forms.

The later Methods subsection now references this representation rather than redefining it. The identity is still described as an exact algebraic reinterpretation of the inherited coefficients, not a separate theorem-level novelty claim.

## 2026-08-13 — Round 2 narrative and structural review

Peer feedback requested a less defensive narrative and a clearer focal result. The reviewed manuscript therefore:

1. rewrites the Abstract to lead with the mismatch insight and retains one concise scope caveat;
2. consolidates six contributions into three: controlled baseline, mismatch/alignment structure, and generic root sensitivity;
3. previews the one-dimensional mismatch collapse in the Introduction;
4. reframes nearby-work discussion positively as a complementary niche;
5. removes repeated `inherited empirical object` disclaimers and uses conditional wording only where needed;
6. removes internal project labels (`N1a`, `N1b`, `Phase 4`, `Phase 13`) from the journal-facing text;
7. adds **Proposition 1 (Conditional mismatch principle)** in Results;
8. adds a Discussion subsection separating the algebraically general weighted-variance identity from the two-agent-specific cubic/factorization analysis;
9. records the risk that a future revision of Ref. [7] would require re-evaluation against an updated Empirical Law 4.3 expression;
10. shortens the Methods AI disclosure and retains the full disclosure in Acknowledgments;
11. adds future-work directions for $n>2$, stochastic settings, and adaptive weighting/compression-aware design;
12. attributes the homogeneous baseline explicitly to **Theorem 3.1 of Ref. [7]**;
13. standardizes the homogeneous-baseline symbol as $\rho_{\mathrm{hom}}$.

## 2026-08-13 — LaTeX/PDF hygiene

Live Overleaf review also exposed template-level warnings. The manuscript now uses PDF-string-safe `\texorpdfstring` fallbacks for mathematical EF$^{21}$ front-matter/heading text, sets a sufficient `\headheight`, and uses a breakable DOI display for the long arXiv DOI entry. These are typesetting/metadata fixes only.

## Scientific review status

Substantive author/peer review is now active. The current manuscript retains the core scientific guardrails: Empirical Law 4.3 is treated as a reproduced source relation; the fixed-average factorization and root-sensitivity conclusions remain scoped to the two-agent inherited cubic; the weighted-moment variance identity is algebraically broader but is not used to claim an arbitrary-$n$ EF$^{21}$ convergence theorem; and absolute novelty claims remain avoided.
