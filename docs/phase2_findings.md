# Phase 2 — Stability Landscape and First Findings

## Scope

This phase evaluates the Empirical Law 4.3 cubic contraction factor over a controlled two-agent heterogeneity path while keeping average strong convexity fixed.

Primary axes:

```text
tau = mu2 / mu1 in [0.05, 1.00]
epsilon in [0.01, 0.95]
```

Conditioning strata:

```text
kappa_bar in {2, 10, 100}
L = 1
mu_bar = 1 / kappa_bar
```

Each stratum contains 96 x 95 = 9,120 cells, for 27,360 cells in total.

## Finding 1 — Heterogeneity has a monotone relative penalty on the studied grid

For all three conditioning strata, the normalized penalty

```text
H_norm = (rho_star - rho_homogeneous) / (1 - rho_homogeneous)
```

decreases as `tau` increases. Since lower `tau` means greater worker heterogeneity, this means stronger heterogeneity is associated with a larger relative deterioration of the empirical contraction margin throughout the sampled domain.

The maximum observed relative penalties occur at the strongest studied heterogeneity (`tau = 0.05`) and highest studied compression error (`epsilon = 0.95`):

| kappa_bar | maximum H_norm |
| ---: | ---: |
| 2 | 5.0736% |
| 10 | 1.6990% |
| 100 | 0.2005% |

These are computational observations of the empirical cubic law, not a proof of global monotonicity outside the sampled domain.

## Finding 2 — Compression amplifies the relative heterogeneity penalty

Within numerical tolerance, `H_norm` is nondecreasing with `epsilon` for every fixed `tau` on the default grids for all three conditioning strata.

The interpretation is relative rather than absolute: stronger compression leaves less contraction margin, so a small absolute heterogeneous gap can consume a larger fraction of the remaining margin.

## Finding 3 — Better-conditioned systems show the larger relative heterogeneity penalty

The ordering of the maximum normalized penalty is

```text
kappa_bar = 2  >  kappa_bar = 10  >  kappa_bar = 100.
```

This is the opposite of a simple expectation that worse baseline conditioning must make heterogeneity relatively more damaging. In the poorly conditioned regime, the homogeneous baseline is already close to unit contraction, so the additional heterogeneous deterioration is small relative to the already dominant baseline difficulty.

This conditioning interaction should be treated as a primary result to test on denser and held-out grids.

## Finding 4 — Absolute and normalized penalties peak in different compression regimes

The largest absolute gaps occur at low-to-moderate compression error:

| kappa_bar | epsilon at maximum absolute penalty | maximum absolute penalty |
| ---: | ---: | ---: |
| 2 | 0.11 | 0.0156497 |
| 10 | 0.08 | 0.00210198 |
| 100 | 0.07 | 0.0000301842 |

By contrast, the normalized penalty is largest at `epsilon = 0.95` in every studied stratum.

This distinction matters. Near unit contraction, both homogeneous and heterogeneous rates are poor, so their absolute difference can be small even when heterogeneity consumes a substantial fraction of the remaining convergence margin. Reporting only the absolute gap would therefore understate the practical importance of heterogeneity under heavy compression.

## Reproducibility

Run the complete Phase 2 analysis with:

```bash
python scripts/analyze_phase2.py
```

The script produces:

- `outputs/phase2/phase2_summary.json`
- `outputs/phase2/strata_summary.csv`
- `outputs/phase2/sensitivity_slices.csv`
- `figures/phase2/rho_landscape_kappa10.svg`
- `figures/phase2/normalized_penalty_kappa10.svg`
- `figures/phase2/conditioning_comparison.svg`

The pinned summary from the default 27,360-cell run is stored in `results/phase2_summary.json`.

## Interpretation guardrails

1. Empirical Law 4.3 remains an empirical law; this phase does not convert it into a theorem.
2. Grid monotonicity does not by itself establish global analytic monotonicity.
3. The fixed-average parameterization isolates heterogeneity from average strong convexity, but it remains a structured two-agent path rather than the full heterogeneous parameter space.
4. Practical parameter-selection rules will be proposed only after denser and held-out validation.

## Next step

Phase 3 should test whether the observed ordering and monotonic patterns survive:

- denser off-grid sampling,
- alternative fixed-average conditioning strata,
- randomized admissible parameter draws,
- and direct comparison against the broader four-parameter two-agent space.

Only after those checks should the project formulate a practical compression or step-size guideline.
