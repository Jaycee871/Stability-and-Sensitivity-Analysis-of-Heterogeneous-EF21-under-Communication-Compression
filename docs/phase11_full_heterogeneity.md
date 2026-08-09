# Phase 11 — Controlled Full-Heterogeneity Extension

## Motivation

Phases 1–10 deliberately fixed `L1=L2` and varied only the local strong-convexity parameters. That design isolated one clean source of heterogeneity and produced an auditable stability/sensitivity characterization, but Empirical Law 4.3 itself allows heterogeneous regularity pairs `(L_i, mu_i)`.

Phase 11 expands the controlled design to the full two-agent regularity setting without changing the status of the inherited law: the cubic remains an inherited empirical object to be characterized, not a theorem that this repository claims to prove.

## Controlled parameterization

Define arithmetic means

- `L_bar = (L1 + L2)/2`,
- `mu_bar = (mu1 + mu2)/2`,
- `kappa_bar = L_bar / mu_bar`.

Introduce two independent heterogeneity ratios

- `tau_L = L2/L1`,
- `tau_mu = mu2/mu1`,

with both ratios in `(0,1]`. Holding `L_bar` and `mu_bar` fixed gives

- `L1 = 2 L_bar/(1+tau_L)`,
- `L2 = 2 L_bar tau_L/(1+tau_L)`,
- `mu1 = 2 mu_bar/(1+tau_mu)`,
- `mu2 = 2 mu_bar tau_mu/(1+tau_mu)`.

This keeps the average condition number fixed while allowing smoothness heterogeneity and strong-convexity heterogeneity to vary independently.

## Important invariant

For the inherited two-agent empirical step size,

`eta_star = 4 / [(L1+mu1)+(L2+mu2)] * (1-s)/(1+s)`,

where `s=sqrt(epsilon)`. Under the controlled Phase 11 parameterization,

`(L1+L2)+(mu1+mu2) = 2(L_bar+mu_bar)`,

so `eta_star` is constant across `(tau_L,tau_mu)` at fixed `(L_bar,mu_bar,epsilon)`.

This is a useful experimental control: changes in the inherited cubic contraction factor arise through the regularity-shape terms `K1` and `K2`, not through a changing empirical step size or changing average condition number.

## Admissible domain

Each local function must satisfy the inherited regularity relation `0 < mu_i <= L_i`. Independent ratio variation therefore creates a conditioning-dependent admissible subset of the square `(tau_L,tau_mu) in (0,1]^2`.

Phase 11 does not silently coerce invalid points. The implementation validates each requested cell and records how many cells are excluded because `mu_i > L_i` for at least one worker.

This boundary is itself scientifically relevant: at poorer or better average conditioning, the geometry of the admissible regularity-heterogeneity region changes.

## Primary Phase 11 questions

1. How does smoothness heterogeneity (`tau_L`) affect the inherited optimal contraction factor when strong-convexity heterogeneity is held fixed?
2. How does strong-convexity heterogeneity (`tau_mu`) behave when smoothness heterogeneity is allowed to vary simultaneously?
3. Does compression amplify aligned and misaligned regularity heterogeneity differently?
4. Are the most sensitive regions concentrated near the local-regularity feasibility boundary `mu_i=L_i`, or elsewhere in the admissible domain?
5. How much of the Phase 1–10 equal-smoothness picture survives on the full `(tau_L,tau_mu)` surface?
6. Does the sign or magnitude of the heterogeneous penalty change when `L_i` and `mu_i` heterogeneity are deliberately mismatched?

## Backward-compatibility checks

The Phase 11 implementation is regression-tested so that:

- `tau_L=1` reproduces the Phase 1–10 equal-smoothness implementation exactly;
- `tau_L=tau_mu=1` recovers the homogeneous theorem baseline;
- scaling `L_bar` and `mu_bar` by the same positive factor leaves the cubic contraction factor unchanged while scaling the empirical step size inversely;
- invalid local regularity configurations are rejected or explicitly masked by the grid runner.

## Initial computational grid

The default Phase 11 runner uses

- 31 values of `tau_L` on `[0.05,1]`,
- 31 values of `tau_mu` on `[0.05,1]`,
- 95 values of `epsilon` on `[0.01,0.95]`,
- `kappa_bar in {2,10,100}`.

This gives 273,885 requested cells before admissibility masking. The first Phase 11 objective is structural mapping and validation; publication-resolution refinement can be increased after the first landscapes identify which regions deserve denser sampling.

## Symbolic follow-up

The existing Wolfram bridge remains available for Phase 11. Symbolic work should begin only after the computational surface is understood. Candidate follow-ups include:

- exact simplification of `K1(tau_L,tau_mu,kappa_bar)` and `K2(tau_L,tau_mu,kappa_bar)`;
- characterization of the admissible boundary `mu_i<=L_i`;
- discriminant sign checks on selected full-heterogeneity strata;
- testing whether any positivity structure from Phase 4 survives after adding `tau_L` as a second symbolic heterogeneity coordinate.

No symbolic observation should be promoted to a global theorem without an explicit proof covering the claimed domain.

## Claim guardrail

Phase 11 is a controlled computational and mathematical extension of an inherited empirical law. It does **not** claim:

- a proof of Empirical Law 4.3;
- a new general EF21 convergence theorem;
- universal monotonicity over all heterogeneous regularity parameters;
- a communication-complexity optimum;
- empirical performance guarantees for arbitrary stochastic machine-learning tasks.
