# Phase 5 — Manuscript and paper-asset plan

## Scope lock

Phase 5 does **not** introduce a new parameter family, a new algorithm, or a broader theorem claim. It packages the audited Phase 1–4 results into a manuscript-ready structure and a reproducible paper-asset pipeline.

## Working title

**Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression**

## Core paper story

1. The source paper gives a two-agent heterogeneous cubic rate as Empirical Law 4.3.
2. The reproduction verifies that law over a large independent grid.
3. The extension fixes average strong convexity and varies only heterogeneity and compression.
4. Dense and off-grid analyses characterize how heterogeneity consumes contraction margin.
5. A retention metric converts the rate landscape into an interpretable operating boundary.
6. A Wolfram symbolic audit shows that the cubic remains in a three-distinct-real-root regime for the three audited conditioning strata.
7. The paper therefore contributes a controlled numerical/mathematical characterization, not a proof of the full empirical law.

## Main figures

### Figure 1 — Contraction landscape

- `rho_star(tau, epsilon)` at `kappa_bar=10`.
- Purpose: establish the overall stability/convergence landscape.

### Figure 2 — Normalized heterogeneity penalty

- `(rho_star-rho_homogeneous)/(1-rho_homogeneous)` at `kappa_bar=10`.
- Purpose: isolate the relative penalty of heterogeneity after controlling average conditioning.

### Figure 3 — Compression × conditioning interaction

- normalized penalty versus `epsilon` at the strongest studied heterogeneity (`tau=0.05`).
- three curves: `kappa_bar=2,10,100`.
- Purpose: show compression amplification and explain the conditioning dependence.

### Figure 4 — 99% contraction-margin retention boundary

- minimum `tau` satisfying `R>=0.99` versus `epsilon`.
- three conditioning strata.
- Purpose: convert the computational characterization into an interpretable operating guideline.

### Figure 5 — Boundary convergence under refinement

- finite-grid 99% boundary estimates versus grid resolution at `epsilon=0.95`, with bisection references.
- Purpose: demonstrate that the practical thresholds are not coarse-grid artifacts.

### Supplementary Figure S1 — Symbolic root structure

- compact statement of the discriminant factorization result.
- Purpose: separate the analytic root-structure result from the main computational figures.

## Main table

`Table 1` summarizes, by conditioning stratum:

- `rho_min`, `rho_max`;
- maximum absolute heterogeneity penalty;
- maximum normalized heterogeneity penalty;
- continuous 99% retention boundary at `epsilon=0.95`;
- whether the full audited `tau>=0.05` domain meets the 99% target.

## Manuscript section map

1. Introduction
2. Background and inherited cubic law
3. Methods
   - controlled fixed-average parameterization
   - conditioning strata
   - outcome metrics
   - dense grid
   - retention boundaries
   - off-grid robustness
   - independent Wolfram audit
4. Results
   - contraction landscape
   - normalized penalty
   - compression/conditioning interaction
   - retention boundaries
   - boundary robustness
   - symbolic root structure
5. Discussion
6. Limitations
7. Conclusion

## Claim discipline

Allowed language:

- computational characterization
- audited parameter domain
- observed monotonic pattern
- bisection reference boundary
- analytic discriminant/root-structure result for fixed strata
- independent symbolic cross-check

Avoid unless separately proved:

- general convergence theorem
- proof of Empirical Law 4.3
- universal stability threshold
- communication-complexity lower bound
- global monotonicity theorem

## Reproducible build

```bash
python scripts/build_paper_assets.py
```

The command writes generated figures and tables under `paper_assets/`. The generator recomputes values from the same Python implementation used by the audited experiments; values are not manually copied into plotting code.
