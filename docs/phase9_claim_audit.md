# Phase 9 — Claim-to-Evidence Audit

Phase 9 turns the manuscript's central quantitative and mathematical statements into an auditable registry. Each registered claim is linked to a version-controlled evidence location and retains an explicit scope guardrail.

## Why this phase exists

A reproducible analysis can still become internally inconsistent if manuscript text is edited independently of result files. The claim registry therefore treats the manuscript and computational evidence as a coupled object: when a headline number, symbolic statement, or scope label changes, the corresponding registry entry must also continue to validate.

## Evidence hierarchy

The audit distinguishes four evidence levels:

1. **Inherited literature** — formulas or status labels inherited from the source paper. These must preserve the source paper's distinction between proved results and empirical laws.
2. **Computational** — finite-grid results and bisection-based operating boundaries produced by the repository analysis.
3. **Computational robustness** — deterministic off-grid stress tests and numerical residual checks. These strengthen a numerical observation but do not prove global monotonicity.
4. **Analytic-symbolic** — exact symbolic consequences established for the explicitly tested fixed-conditioning strata using the independent Wolfram implementation.

## Registered manuscript claims

The first registry version covers nine headline claims:

- C01 — 216,027 controlled configurations;
- C02 — maximum normalized heterogeneity penalties by conditioning stratum;
- C03 — compression-amplification ratios at `tau=0.05`;
- C04 — slow-region prevalence for `kappa_bar=100`;
- C05 — continuous 99% retention boundaries at `epsilon=0.95`;
- C06 — off-grid robustness and root-residual audit;
- C07 — 63 strictly positive discriminant-polynomial coefficients for each tested stratum;
- C08 — three distinct real roots on each tested open controlled domain;
- C09 — inherited Empirical Law 4.3 status of the cubic and step-size expressions.

## Automated audit

Run:

```bash
python scripts/audit_claim_registry.py
```

The command validates manuscript anchors and evidence values and writes:

```text
results/phase9_claim_audit.json
docs/claim_evidence_matrix.md
```

CI runs the same audit to a temporary directory and uploads the generated matrix as a workflow artifact. The build fails if a registered manuscript statement can no longer be reconciled with its declared evidence.

## Important guardrails

- A finite-grid maximum is not called a global analytic maximum.
- A bisection operating boundary is not called a universal stability threshold.
- The small positive `kappa_bar=100` off-grid epsilon-ordering residual (~`3.7e-10`) is explicitly retained and interpreted under the project's `1e-9` numerical tolerance rather than silently rounded away.
- The positive-discriminant result is restricted to `kappa_bar in {2,10,100}`.
- Three distinct real roots do **not** constitute a proof of Empirical Law 4.3 as a general EF21 convergence theorem.

The registry is designed to support both manuscript quality control and rapid reviewer-response preparation.
