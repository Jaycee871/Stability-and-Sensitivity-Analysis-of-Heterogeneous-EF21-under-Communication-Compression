# Phase 16 — Cross-Model Novelty Refinement and Reference-Closure Gate

## Why Phase 16 exists

Phase 15 adjudicated the first Undermind shortlist. A second targeted audit from Claude Sonnet 5, together with its supplied chain-of-thought/search-process notes, sharpens the novelty boundary further.

The most important correction is to split the former N1 claim into an inherited algebraic reinterpretation and a potentially novel controlled factorization.

## N1a — inherited weighted-variance identity

From the inherited Empirical Law 4.3 definitions,

\[
q_i=\frac{\Delta_i}{\Sigma_i},\qquad
w_i=\frac{\Sigma_i}{\Sigma_1+\Sigma_2},
\]

we have

\[
K_1=\sum_i w_i q_i^2,
\qquad
K_2=\left(\sum_i w_i q_i\right)^2,
\]

hence

\[
K_1-K_2=\operatorname{Var}_w(q_i).
\]

Wolfram independently simplifies the residuals for the weighted-second-moment identity, weighted-mean identity, and variance identity to zero.

**Novelty status:** none claimed. This is an exact algebraic reinterpretation of inherited quantities. Its contribution is explanatory, not theorem-level novelty.

Unsafe wording:

> We introduce a novel weighted-variance heterogeneity measure for EF21.

Safe wording:

> The inherited coefficients admit the exact interpretation \(K_1-K_2=\operatorname{Var}_w(q_i)\).

## N1b — fixed-average explicit mismatch factorization

Under the Phase 11 controlled parameterization with fixed \(\bar L\) and \(\bar\mu\), define

\[
\bar\kappa=\frac{\bar L}{\bar\mu},\qquad
\tau_L=\frac{L_2}{L_1},\qquad
\tau_\mu=\frac{\mu_2}{\mu_1}.
\]

Then Phase 12 derives

\[
K_1-K_2=
\frac{4\bar\kappa^2(\tau_L-\tau_\mu)^2}
{(\bar\kappa+1)^2
(\tau_L+\bar\kappa\tau_\mu+\bar\kappa+1)
(\bar\kappa\tau_L\tau_\mu+\tau_L\tau_\mu+\bar\kappa\tau_L+\tau_\mu)}.
\]

An independent Wolfram simplification of the Phase 12 expression against the inherited \(K_1-K_2\) returns zero.

**Novelty status:** plausible, not closed. The supplied cross-model searches report no theorem-level equivalent, but the backward citation chain of the source paper has not yet been completely inspected primary-source-by-primary-source.

## N2 — aligned proportional heterogeneity

The explicit factorization gives

\[
K_1-K_2=0\iff \tau_L=\tau_\mu
\]

on the admissible positive domain. Along this aligned path, the inherited cubic coefficients coincide with the homogeneous controlled coefficients at the same average conditioning and compression.

**Novelty status:** plausible, not closed. No algebraically equivalent theorem was reported in the targeted search. Colla and Hendrickx provide useful PEP/two-agent context but not an equivalent result.

## N3 — strict largest-root mismatch sensitivity

Phase 13 proves, conditional on the inherited empirical cubic,

\[
\frac{d\rho^\star}{dK_1}>0.
\]

The Claude search identified control/spectral monotonicity papers as method templates but reported no same-axis result for inter-agent regularity mismatch.

**Novelty status:** plausible, not closed. The proof technique is not itself novel; only the result in this inherited cubic coordinate system is under novelty audit.

## N4 — generic cubic root structure

Phase 13 certifies on the stated generic shape domain that the inherited cubic has three distinct real roots in \((0,1)\), and that the selected largest root satisfies \(\rho^\star>s=\sqrt\epsilon\).

The targeted search reports no equivalent prior theorem and notes that the source paper does not provide this generic root-structure analysis.

**Novelty status:** plausible, not closed.

## Refined prior-art classification

- **Thomsen–Taylor–Dieuleveut (2026): ANCHOR.** The empirical law, \(K_1\), \(K_2\), and the cubic are inherited. N1a is therefore not a novelty claim.
- **Richtárik–Gasanov–Burlachenko (2024): Class C with wording constraint.** Their variance-like quantity concerns smoothness heterogeneity \(L_i\) alone and is not an algebraic equivalent of the paired condition-shape mismatch. However, it prevents broad wording such as “first variance-based EF21 heterogeneity characterization.”
- **Colla–Hendrickx (2024): Class C.** Useful PEP/agent-symmetry context and a nearby but non-equivalent conjecture for EXTRA.
- **Original EF21, EControl, Tian–Chai–Xu, Patel et al.: provenance/method context only for N1b–N4 under the supplied audit.** No same-axis theorem-level equivalence was reported.

## What the supplied Claude chain-of-thought changes

The search-process notes are scientifically useful because they expose uncertainty that a polished final answer can hide:

1. the search covered roughly fifteen targeted queries rather than an exhaustive literature universe;
2. several source-paper references were not individually opened and adjudicated;
3. some conclusions were based on absence of hits rather than a closed citation graph;
4. the statement that the researcher already possessed a separate Jury-criterion derivation for heterogeneous compression gains was an inference/recall by the model, not an independently located source in the connected repository.

Therefore the Claude report is retained as **search evidence**, not as a novelty certificate.

## Unresolved cross-model reference

Claude's notes mention an `[[ef21-stability-analysis]]` project with a Jury analysis of heterogeneous compression gains and a `c0` invariant. A search of the current connected repository did not locate a concrete file, path, or commit matching that description.

Status:

```text
UNRESOLVED_CROSS_MODEL_REFERENCE
```

It must not be cited or used as scientific evidence unless a concrete source is located later.

## Reference-closure checklist

Before novelty language is promoted into the manuscript, individually inspect and record exact theorem/equation/page evidence for the source-paper related-work items that Claude explicitly marked as not yet checked in full:

- Zheng 2019
- Li & Li 2022
- Tang 2021
- Fatkhullin 2023/2025
- Condat 2022
- Gruntkowska 2025
- Egger 2025
- Redie 2026
- Tian 2026

The exact bibliography identity of each item must be resolved from the source paper before adjudication; names/years in the model report are not sufficient identifiers on their own.

## Manuscript gate

Until that closure is complete:

- N1a may be described as an exact inherited algebraic reinterpretation;
- N1b–N4 may be described internally as **novelty-plausible candidate contributions**;
- no “first”, “novel”, “for the first time”, or universal absence-of-prior-work wording may be inserted into the manuscript.

This phase strengthens the paper by narrowing novelty rather than maximizing it.
