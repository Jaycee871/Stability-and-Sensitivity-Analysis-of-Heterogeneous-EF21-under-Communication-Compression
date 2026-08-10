# Phase 21 — Claim Registry v2

## Purpose

The original Phase 9 registry covered the equal-smoothness baseline only. Phases 11–20 added a second scientific layer—full local regularity heterogeneity, structural mismatch coordinates, generic symbolic root sensitivity, primary-source literature closure, and publication figures. Phase 21 updates the claim-to-evidence system so that the manuscript cannot contain those newer claims without a machine-checkable evidence path.

## Registry expansion

Registry version 2 contains 18 claims.

### C01–C09 — retained baseline claims

These preserve the original dense-grid, retention-boundary, robustness, fixed-stratum symbolic, and inherited-literature evidence.

The former generic `analytic-symbolic` label is split into the more precise `analytic-symbolic-fixed-strata` for the Phase 4 discriminant claims.

### C10 — full-regularity grid accounting

Links the manuscript's `273,885` requested and `258,400` admissible cells to `results/phase12_summary.json`.

### C11 — K2 invariance

Links the fixed-average identity

\[
K_2=\left(\frac{\bar\kappa-1}{\bar\kappa+1}\right)^2
\]

to the Phase 13 symbolic certificate.

### C12 — inherited weighted-variance interpretation

Links

\[
K_1-K_2=\operatorname{Var}_w(q_i)
\]

to both the Phase 12 algebraic audit and the Phase 17 explicit `NO_NOVELTY` classification. This row exists partly to prevent the explanatory rewrite from being promoted into a novelty claim.

### C13 — controlled mismatch factorization

Links the exact fixed-average rational factorization and its `(tau_L-tau_mu)^2` numerator factor to the Phase 13 structural certificate.

### C14 — aligned proportional-heterogeneity invariance

Links `tau_L=tau_mu` to both zero mismatch and equality with the homogeneous controlled cubic.

### C15 — generic cubic root structure

Links the manuscript statement that the inherited cubic has three distinct real roots in `(0,1)` and `rho_star>sqrt(epsilon)` to the generic Wolfram certificate rather than the earlier fixed-stratum factorization.

### C16 — largest-root sensitivity

Links

\[
\frac{d\rho^\star}{dK_1}>0
\]

to the Phase 13 implicit-derivative and largest-root sign certificate.

### C17 — controlled rate consequence

Links the statement that the aligned path minimizes the inherited largest-root prediction to the Phase 13 combination of the mismatch factorization and root sensitivity.

### C18 — literature-audit boundary

Links the manuscript's scoped prior-art wording to the Phase 17 closure record:

```text
NAMED_REFERENCE_CHAIN_CLOSED
universal_novelty_certified = false
named_sources_checked = 12
direct_equivalents_to_N1b_N4 = 0
```

The row is deliberately a **literature-audit claim**, not a novelty certificate.

## Evidence hierarchy

Version 2 distinguishes:

- inherited literature;
- inherited algebraic interpretation;
- controlled algebraic consequences;
- finite computational grids;
- computational robustness;
- fixed-stratum symbolic analysis;
- generic inherited-cubic symbolic analysis;
- controlled consequences combining symbolic and algebraic layers;
- scoped primary-source literature audit.

This prevents evidence-strength drift. A symbolic proof about the inherited cubic cannot silently become a proof of EF21, and a closed named bibliography chain cannot silently become universal bibliographic novelty.

## CI behavior

The Phase 21 CI step runs:

```bash
python scripts/audit_claim_registry.py \
  --output-json /tmp/phase21/phase21_claim_audit.json \
  --output-md /tmp/phase21/claim_evidence_matrix.md
```

Every registered claim must satisfy both conditions:

1. its exact manuscript anchor is still present;
2. all version-controlled evidence checks still pass.

The generated claim matrix is also copied into the reviewer pre-mortem artifact.

## Guardrail

A passing registry means the manuscript statements are traceable to the recorded evidence at their stated scope. It does **not** mean every statement is a theorem, that Empirical Law 4.3 has been proved, or that universal novelty has been established.
