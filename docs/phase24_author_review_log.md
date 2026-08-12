# Phase 24 author review log

## 2026-08-11 — Authorship order

Author review established the current manuscript order as:

1. **Pack Kwan Low** — first author.
2. **Fu-Hsing Wang** — second author and corresponding author.

The authorship correction changes front matter and submission metadata only. It does not modify the scientific claims, numerical results, symbolic analysis, figures, references, or the manuscript's two-agent / Empirical Law 4.3 scope guardrails.

## 2026-08-11 — EF$^{21}$ notation and first-use expansion

Author review requested the algorithm name be typeset as `EF$^{21}$` rather than plain `EF21`.

The first wording request was to expand `EF` as **Error Feedback** at the first visible occurrence. A follow-up clarification immediately refined the first-use wording to the full name **Error Feedback 21**. Accordingly, because the manuscript title is the first visible occurrence, the current author-reviewed title is staged as:

**Stability and Sensitivity Analysis of Heterogeneous Error Feedback 21 (EF$^{21}$) under Communication Compression**

Subsequent visible manuscript uses are typeset as `EF$^{21}$`. Bibliographic titles, citation keys, filenames, and source identifiers are not mechanically rewritten. In particular, published titles that formally use plain `EF21` remain verbatim in the References section.

This is an editorial terminology/typesetting correction only. It does not alter the scientific claims, equations, numerical results, symbolic analysis, figures, references, or the inherited two-agent Empirical Law 4.3 scope.

## 2026-08-12 — First-use technical-term emphasis

Author review requested that technical terms be italicized at their first manuscript occurrence. The implementation is deliberately conservative: first-use emphasis is applied to concepts the manuscript explicitly distinguishes or defines, while proper names, algorithm names, theorem/law labels, acronyms, and formal bibliographic titles remain in their standard typography.

The current guarded first-use emphasis includes the manuscript's initial uses of *statistical or data heterogeneity*, *regularity heterogeneity*, *local condition-shape coordinates*, *aligned heterogeneity*, and *regularity mismatch*. Later occurrences remain un-emphasized.

## 2026-08-12 — $K_1$ / $K_2$ reader guidance

Author review asked what the inherited coefficients $K_1$ and $K_2$ represent. Their exact weighted-moment interpretation is already derived later in Methods, where $K_1$ is a weighted second moment, $K_2$ is the squared weighted mean, and $K_1-K_2$ is the corresponding weighted variance.

To prevent the first Background occurrence from being formula-only, the manuscript now adds the following one-sentence preview immediately after the inherited definitions:

> These coefficients summarize the weighted second moment and squared weighted mean of the local condition-shape coordinates; their difference will later be shown to equal a weighted variance.

This is reader guidance only. It does not modify the inherited definitions, the later algebraic identity, or any scientific claim.

## Scientific review status

Line-by-line author review has begun with authorship, notation, acronym/full-name, typography, and coefficient-interpretation comments. Detailed mathematical/scientific review remains pending further comparison with the source paper *A Tight Theory of Error Feedback Algorithms in Distributed Optimization*. Until substantive scientific comments are received, Phase 24 keeps the scientific body frozen except for explicit author-review edits and necessary metadata/integrity corrections.
