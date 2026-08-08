# Phase 3 — Interaction Analysis and Practical Guidelines

## Purpose

Phase 3 converts the Phase 2 stability landscape into interpretable, grid-backed operating guidance without claiming a new convergence theorem.

The dense default study evaluates

- 381 heterogeneity ratios `tau` from 0.05 to 1.00,
- 189 compression errors `epsilon` from 0.01 to 0.95,
- three fixed average condition-number strata `kappa_bar in {2, 10, 100}`,
- for a total of **216,027 parameter cells**.

Average strong convexity remains fixed within each stratum, so the comparison continues to isolate heterogeneity from average conditioning.

## 1. Contraction-margin retention

Phase 2 defined the normalized heterogeneity penalty as

```text
H_norm = (rho_star - rho_homogeneous) / (1 - rho_homogeneous).
```

Phase 3 uses the equivalent retention quantity

```text
R = (1 - rho_star) / (1 - rho_homogeneous)
  = 1 - H_norm.
```

`R` therefore has a direct interpretation: it is the fraction of the homogeneous contraction margin that remains after introducing the studied heterogeneity.

A `99% retention` guideline means `H_norm <= 0.01`; `98% retention` means `H_norm <= 0.02`; and `95% retention` means `H_norm <= 0.05`.

## 2. Dense-grid guideline boundaries

For each compression level and conditioning stratum, the code finds the smallest studied `tau` whose normalized penalty stays below a specified limit. The boundary is reported only because the tested penalty is nonincreasing as `tau` increases on the grid; a monotonicity failure invalidates boundary construction.

Selected 99% retention boundaries are:

| `epsilon` | `kappa_bar=2` | `kappa_bar=10` | `kappa_bar=100` |
| ---: | ---: | ---: | ---: |
| 0.05 | 0.2450 | 0.0500 | 0.0500 |
| 0.20 | 0.3375 | 0.1325 | 0.0500 |
| 0.50 | 0.3825 | 0.1675 | 0.0500 |
| 0.80 | 0.4025 | 0.1775 | 0.0500 |
| 0.95 | 0.4100 | 0.1800 | 0.0500 |

Thus, within the studied domain, stronger compression requires a progressively less heterogeneous pair to preserve 99% of the homogeneous contraction margin when average conditioning is good or moderate.

For 98% retention, the `kappa_bar=10` and `kappa_bar=100` strata satisfy the target over the full studied `tau >= 0.05` domain. At `kappa_bar=2`, the minimum `tau` at `epsilon=0.95` is approximately 0.26.

For 95% retention, almost the entire studied domain satisfies the target. The only dense-grid adjustment among the selected extreme settings is `kappa_bar=2, epsilon=0.95`, where the boundary moves from the domain minimum 0.05 to approximately 0.055.

These are **computational operating boundaries on the specified grid**, not universal analytic thresholds.

## 3. Compression amplifies the relative heterogeneity burden

At the maximum studied heterogeneity (`tau=0.05`), increasing compression error from `epsilon=0.01` to `epsilon=0.95` increases the normalized heterogeneity penalty by:

| `kappa_bar` | penalty at 0.01 | penalty at 0.95 | multiplicative change |
| ---: | ---: | ---: | ---: |
| 2 | 1.3207% | 5.0736% | 3.841x |
| 10 | 0.5446% | 1.6990% | 3.120x |
| 100 | 0.0661% | 0.2005% | 3.033x |

This supports a computational interaction statement: heavier compression increases the **fraction of the remaining homogeneous contraction margin lost to heterogeneity** across all three studied conditioning strata.

The statement is deliberately made in normalized-margin terms. Phase 2 showed that the absolute contraction-factor gap can peak at low-to-moderate compression instead of at the heaviest compression.

## 4. Why the heterogeneity penalty looks smaller at poor conditioning

The declining normalized penalty from `kappa_bar=2` to `100` should not be read as evidence that poorly conditioned systems are intrinsically more robust.

The dense-grid slow-region summary is:

| `kappa_bar` | fraction `rho_star >= 0.90` | fraction `rho_star >= 0.95` | fraction `rho_star >= 0.99` |
| ---: | ---: | ---: | ---: |
| 2 | 23.99% | 10.19% | 0.00% |
| 10 | 68.48% | 40.86% | 6.03% |
| 100 | 100.00% | 100.00% | 63.49% |

At `kappa_bar=100`, the baseline problem is already close to unit contraction throughout the studied domain. Consequently, there is little remaining contraction margin for heterogeneity to remove. The smaller normalized heterogeneity penalty is therefore best interpreted together with the much slower baseline convergence landscape.

## 5. Practical interpretation

The Phase 3 guideline is not "choose tau" in a deployed system; `tau` describes an observed curvature ratio rather than a tunable algorithm parameter. Instead, the boundary answers a planning question:

> Given an estimated heterogeneity ratio and average conditioning, how much compression can be tolerated while retaining a chosen fraction of the homogeneous contraction margin predicted by the empirical cubic law?

This can support compressor selection or communication-budget decisions. A system whose estimated `(kappa_bar, tau)` lies below a desired retention boundary should use weaker compression if preserving that margin is important.

## Guardrails

- All boundaries are finite-grid computational characterizations of Empirical Law 4.3.
- The study does not establish global monotonicity outside the tested domain.
- `tau` is a descriptive heterogeneity parameter, not a control knob.
- A small normalized heterogeneity penalty does not imply fast convergence; absolute `rho_star` must also be inspected.
- Future empirical use should estimate curvature quantities carefully rather than treating the synthetic two-agent parameterization as a direct data-generating model.
