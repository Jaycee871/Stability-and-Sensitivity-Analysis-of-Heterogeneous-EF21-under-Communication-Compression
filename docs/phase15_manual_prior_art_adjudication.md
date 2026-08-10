# Phase 15 — Manual Prior-Art Adjudication of the Undermind N1–N2 Shortlist

## Scope

Phase 14 deliberately blocked novelty promotion until an adversarial external search was completed. Undermind returned a seven-paper N1–N2 shortlist. Phase 15 manually adjudicates that shortlist at the theorem/equation level.

This phase is **not** a global proof of novelty. It answers a narrower question:

> Within the supplied adversarial N1–N2 shortlist, is there a prior result algebraically or theorem-level equivalent to the Phase 12 weighted mismatch coordinate or the aligned proportional-heterogeneity invariance?

The answer after manual source inspection is: **no Class-A equivalent was identified in this seven-paper shortlist**. Two papers require explicit positioning as Class B; five are contextual Class C.

N3 (strict largest-root sensitivity) and N4 (generic cubic root structure) are **not cleared by this export** and remain blocked pending a dedicated search.

## Claims under adjudication

### N1 — weighted mismatch variance

Under fixed arithmetic means,

\[
K_1-K_2
=
\operatorname{Var}_{w}
\left(
q_i
\right),
\qquad
q_i=\frac{L_i-\mu_i}{L_i+\mu_i},
\qquad
w_i=\frac{L_i+\mu_i}{\sum_j(L_j+\mu_j)}.
\]

For two workers this is also the exact nonnegative rational mismatch formula derived in Phase 12.

### N2 — aligned proportional-heterogeneity invariance

When

\[
\tau_L=\tau_\mu,
\]

each worker's pair \((L_i,\mu_i)\) is scaled proportionally. Then \(K_1=K_2\), the empirical step size is unchanged, and the inherited Empirical Law 4.3 cubic coincides with the homogeneous controlled cubic at the same average conditioning and compression.

## Adjudication classes

- **A — direct prior art:** algebraically equivalent result or theorem that directly implies the claim under specialization.
- **B — material overlap:** mathematically related result that constrains novelty wording but is not equivalent.
- **C — contextual adjacency:** relevant EF21/error-feedback/Lyapunov/distributed-rate literature without the same structural result.
- **D — superficial overlap:** similar terminology without mathematical bearing on N1–N2.

## Candidate-by-candidate decision

| Candidate | Class | N1/N2 relevance | Decision |
|---|---:|---|---|
| Thomsen, Taylor & Dieuleveut (2026), *A Tight Theory of Error Feedback Algorithms in Distributed Optimization* | **B** | Direct source of Empirical Law 4.3, including \(K_1,K_2\) and the cubic | **Anchor prior art.** The algebraic objects are inherited and must never be presented as new. The inspected source does not state the weighted-variance reduction of \(K_1-K_2\) or the proportional-scaling invariance. |
| Thomsen, Taylor & Dieuleveut (2025), *Tight analyses of first-order methods with error feedback* | C | Tight EF/EF21 methodology, but simplified single-agent analysis | No two-agent regularity-mismatch coordinate or N2 invariance. |
| Richtárik, Sokolov & Fatkhullin (2021), *EF21* | C | Foundational EF21 theory and distributed heterogeneity | Necessary provenance, but no equivalent \(K_1-K_2\) condition-shape variance or proportional paired-\((L_i,\mu_i)\) invariance identified. |
| Richtárik, Gasanov & Burlachenko (2024), *Error Feedback Reloaded* | **B** | Heterogeneous smoothness, smoothness-dependent weighting, arithmetic-vs-quadratic means, and a variance-like \(L_{\rm var}=L_{\rm QM}^2-L_{\rm AM}^2\) quantity | **Material novelty constraint.** We must not claim the first variance-style heterogeneity characterization for EF21. Its quantity concerns \(L_i\)-heterogeneity alone and was not found to be algebraically equivalent to the paired condition-shape variance in N1. |
| Upadhyaya et al., *Automated tight Lyapunov analysis for first-order methods* | C | Generic component-wise smooth/strong-convex interpolation and quadratic Lyapunov machinery | Methodological adjacency; no EF21-specific N1/N2 identity identified. |
| Condat, Yi & Richtárik (2022), *EF-BV* | C | Error feedback plus variance-reduction terminology | The relevant variance is compressor/randomness variance, not the weighted dispersion of local condition-shape ratios. |
| Sundararajan, Van Scoy & Lessard (2019), distributed first-order methods over time-varying graphs | C | Exact/worst-case rate analysis using condition number and graph spectral gap | Rate-analysis context only; no N1/N2 algebraic equivalent identified. |

## What survives the adversarial N1–N2 audit

### N1 status: `PROMOTE_WITH_PRIOR_ART_POSITIONING`

The exact claim that survives is **not**:

> EF21 has never been analyzed using a variance-like heterogeneity quantity.

That wording is unsafe because *Error Feedback Reloaded* already contains a variance-like smoothness-dispersion quantity and uses smoothness-dependent weighting.

The narrower structural result supported by the current audit is:

> Starting from the inherited two-agent Empirical Law 4.3, fixed arithmetic means make \(K_2\) invariant and reduce the remaining regularity dependence to \(K_1-K_2\), which is exactly the \(\Sigma_i\)-weighted variance of the local condition-shape ratios \(q_i=(L_i-\mu_i)/(L_i+\mu_i)\).

This is a characterization of the **inherited empirical law**, not a claim that the original cubic or EF21 itself is newly derived.

### N2 status: `PROMOTE_WITH_PRIOR_ART_POSITIONING`

The current shortlist contains no identified theorem/lemma equivalent to:

> proportional local regularity scaling, \(\tau_L=\tau_\mu\), is invisible to the inherited cubic at fixed average conditioning and compression.

The original 2026 paper remains the closest prior art because it supplies the cubic from which the result follows. Therefore the safe wording is that N2 is an **algebraic structural consequence of the inherited Empirical Law 4.3 under the controlled fixed-average parameterization**.

## What is still blocked

### N3 — monotone rate penalty

Phase 13 proves, conditional on the inherited cubic, that

\[
\frac{d\rho^\star}{dK_1}>0
\]

on the generic shape-coordinate domain. The current Undermind export was designed primarily for N1–N2 and does not constitute a complete adversarial search for equivalent spectral-radius/root-sensitivity results.

Status: `REQUIRES_MANUAL_EQUIVALENCE_CHECK`.

### N4 — generic cubic root structure

Phase 13 also certifies the generic root-location/discriminant structure used in the sensitivity proof. The present shortlist does not constitute a dedicated search over polynomial-root, PEP, IQC, or exact spectral analyses.

Status: `REQUIRES_MANUAL_EQUIVALENCE_CHECK`.

## Candidate manuscript wording after the current partial audit

The following wording is staged, **not yet inserted into the manuscript**:

> Building on the inherited two-agent Empirical Law 4.3, we show that under fixed arithmetic means its regularity dependence admits a one-coordinate structural reduction: \(K_2\) is invariant, while \(K_1-K_2\) is the nonnegative \(\Sigma_i\)-weighted variance of \(q_i=(L_i-\mu_i)/(L_i+\mu_i)\). Consequently, proportional local regularity heterogeneity leaves the inherited cubic unchanged, whereas mismatch between smoothness and strong-convexity heterogeneity activates the structural penalty coordinate. This characterization should be distinguished from prior EF21 analyses of smoothness heterogeneity and variance-like smoothness dispersion.

Do **not** prepend “for the first time” or “the first” until the remaining N3–N4 audit and the final reference review are complete.

## Reproducibility

The original Undermind CSV is archived at:

```text
literature/undermind/Adversarial_N1_N2_Novelty_Audit.csv
```

The machine-readable adjudication is stored in:

```text
literature/phase14_candidate_matrix.json
```

The matrix records the classification, source-check status, overlap dimensions, and per-claim promotion status.

## Guardrail

Absence of a Class-A match in seven candidates is **not evidence of universal novelty**. It is evidence that this supplied adversarial shortlist did not falsify N1 or N2 at theorem/equation level.

The paper must continue to state that Empirical Law 4.3, its cubic, and the definitions of \(K_1,K_2\) are inherited from Thomsen, Taylor, and Dieuleveut. The project contributes a controlled structural characterization and conditional analysis of that inherited empirical object.
