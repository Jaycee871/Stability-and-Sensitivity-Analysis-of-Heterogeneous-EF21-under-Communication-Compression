# Phase 17 — Primary-Source Reference Closure

## Purpose

Phase 16 exposed a concrete bibliographic gap: the second cross-model audit had searched broadly but had not individually opened every paper in the source paper's nearby EF/error-feedback citation chain. Phase 17 closes that **named** chain using primary sources and separates three different statements that must not be conflated:

1. a paper did not appear in a keyword search;
2. a paper was opened and its problem assumptions exclude the target local-regularity structure;
3. universal novelty has been proved.

Only (2) is established here for the named chain. Statement (3) is not claimed.

## Target structure

The candidate contributions remain:

- **N1a — inherited interpretation only:**
  \(K_1-K_2=\operatorname{Var}_w(q_i)\), with \(q_i=(L_i-\mu_i)/(L_i+\mu_i)\). No novelty claim.
- **N1b — fixed-average factorization:** the exact \((\bar\kappa,\tau_L,\tau_\mu)\) rational factorization with the \((\tau_L-\tau_\mu)^2\) factor.
- **N2 — aligned proportional heterogeneity:** \(\tau_L=\tau_\mu\) makes the inherited mismatch coordinate vanish and recovers the homogeneous controlled cubic.
- **N3 — largest-root sensitivity:** conditional on the inherited cubic, \(d\rho^\star/dK_1>0\).
- **N4 — generic root structure:** three distinct real roots in \((0,1)\) and \(\rho^\star>\sqrt\epsilon\) on the stated generic cubic-coordinate domain.

## Primary-source exclusions

### Thomsen, Taylor & Dieuleveut (2026) — anchor

This is the source of Empirical Law 4.3, \(K_1\), \(K_2\), and the cubic. It must be cited as the anchor rather than treated as a novelty conflict. The project does **not** claim those inherited objects as new.

### Zheng, Huang & Kwok (2019)

The paper analyzes distributed blockwise SGD/momentum with error feedback on nonconvex objectives. Its Section 3.1 assumptions use a single global smoothness constant \(L\) for \(F\), bounded stochastic-gradient variance, and a gradient bound. There is no family of local strong-convexity parameters \(\mu_i\). Therefore it cannot instantiate N1b or N2, and it contains no matching Empirical-Law-4.3 cubic for N3/N4.

### Li & Li (2022/2023)

The paper is explicitly about federated **nonconvex** optimization with biased compression, data heterogeneity, partial participation, and stale error compensation. Its heterogeneity is statistical/client-data heterogeneity rather than simultaneous local \((L_i,\mu_i)\) regularity heterogeneity.

### Tang et al. (2021)

ErrorCompensatedX concerns error compensation for variance-reduced stochastic algorithms. The variance object is associated with stochastic-gradient history/variance reduction, not the dispersion of local condition-shape ratios. No \(K_1,K_2\) or matching two-agent cubic is introduced.

### Fatkhullin, Tyurin & Richtarik (2023)

Momentum Provably Improves Error Feedback! addresses the canonical stochastic nonconvex setting and removes large-batch limitations using momentum. It does not provide simultaneous local strong-convexity constants \(\mu_i\) paired with local \(L_i\) as the structural axis of the analysis.

### Condat, Yi & Richtarik (2022)

EF-BV unifies error feedback and variance reduction across biased and unbiased compressor classes. Its central variance/bias parameters concern the compression mechanism/randomness, not \(\operatorname{Var}_w((L_i-\mu_i)/(L_i+\mu_i))\). It is retained as Class C method-family context.

### Fatkhullin et al. (2025), EF21 with Bells & Whistles

The paper develops six EF21 extensions: partial participation, stochastic approximation, variance reduction, proximal setting, momentum, and bidirectional compression, with theory in smooth nonconvex and PL-type regimes. No same-axis paired local-regularity mismatch coordinate or Empirical-Law-4.3 cubic result was identified.

### Gao, Islamov & Stich (2023), EControl

This is the strongest near-neighbor exclusion. Section 3, Assumption 1 allows each local objective to have its own smoothness constant \(L_i\). However, Assumption 2 imposes a **single** strong-convexity constant \(\mu\) on the average objective \(f\), and the authors explicitly note that the individual \(f_i\) need not be strongly convex and may even be nonconvex. Thus EControl does not instantiate simultaneous local \((L_i,\mu_i)\) regularity heterogeneity.

### Gruntkowska et al. (2025/2026)

EF21-Muon moves error feedback into non-Euclidean LMO-based optimization and studies non-Euclidean smooth and \((L^0,L^1)\)-smooth settings, including layer-wise generalized smoothness. This is a different geometry/regularity regime from the Euclidean local \((L_i,\mu_i)\) structure of N1b-N4.

### Egger et al. (2025), BICompFL

BICompFL studies stochastic/Bayesian federated learning with bidirectional compression and communication-cost tradeoffs. It does not provide the paired local regularity coordinates or cubic structure relevant here.

### Redie, Arablouei & Werner (2026), SA-PEF

SA-PEF studies nonconvex federated optimization under data heterogeneity and partial participation. Its residual contraction factor is controlled by a step-ahead parameter and belongs to an error-residual recursion; it is not the largest root of Empirical Law 4.3.

### Tian et al. (2026), EF21-RR

EF21-RR studies nonconvex stochastic federated optimization with random reshuffling and extends results to a global PL condition. Its contribution is rate/sample efficiency rather than simultaneous local \((L_i,\mu_i)\) mismatch or the inherited cubic's root structure.

## Closure decision

The named reference chain is now recorded as:

```text
NAMED_REFERENCE_CHAIN_CLOSED
```

No paper in this named chain was found to be algebraically or theorem-level equivalent to N1b-N4.

This does **not** certify universal novelty. It means the concrete unresolved bibliography list generated in Phase 16 has been closed at primary-source scope.

## Manuscript gate

Phase 17 changes the manuscript gate in a deliberately asymmetric way.

### Allowed now

Scoped contribution statements such as:

> Under fixed arithmetic-mean regularity, we derive an explicit factorization of the inherited mismatch coordinate in \((\bar\kappa,\tau_L,\tau_\mu)\).

> We show that proportional smoothness/strong-convexity heterogeneity leaves the inherited two-agent cubic unchanged at fixed average conditioning and compression.

> Conditional on Empirical Law 4.3, we establish a generic largest-root sensitivity result with respect to the mismatch coordinate.

### Still blocked

Do not use:

- `first`
- `novel`
- `for the first time`
- `no prior work`
- any wording implying the polynomial/Jury/Routh/discriminant/implicit-function techniques themselves are new.

The safe contribution is a new **analysis of an inherited empirical object**, not a newly proved EF21 convergence theorem.

## Cross-model reference guardrail

The unresolved `[[ef21-stability-analysis]]` / Jury / `c0` reference remains quarantined. Phase 17 does not use it. A concrete repository path, file, commit, or external source is required before it can enter the scientific evidence chain.
