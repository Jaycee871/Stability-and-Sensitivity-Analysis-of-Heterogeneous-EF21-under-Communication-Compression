# Phase 4 — Robustness and Symbolic Structure

## Purpose

Phase 4 asks whether the Phase 2/3 stability and retention findings survive away from the regular parameter grid, and whether the empirical-law cubic contains symbolic structure that can be certified without turning the project into a full proof of Empirical Law 4.3.

The audited computational domain remains

- `tau in [0.05, 1]`,
- `epsilon in [0.01, 0.95]`,
- `kappa_bar in {2, 10, 100}`,
- `L = 1`, `mu_bar = 1/kappa_bar`.

No monotonicity or guideline claim is extrapolated beyond that domain.

## 1. Off-grid robustness

For each conditioning stratum, 20,000 deterministic random paired samples were drawn inside the audited domain. Each sample checks both:

1. a pair `tau_a < tau_b` at common `epsilon`, where the normalized heterogeneity penalty should not increase when heterogeneity is reduced; and
2. a pair `epsilon_a < epsilon_b` at common `tau`, where the normalized heterogeneity penalty should not decrease when compression error increases.

The maximum observed one-sided violations were:

| `kappa_bar` | max tau violation | max epsilon violation | max cubic-root residual |
| ---: | ---: | ---: | ---: |
| 2 | -1.49e-8 | -4.20e-12 | 2.00e-15 |
| 10 | -1.14e-8 | -2.64e-13 | 1.89e-15 |
| 100 | -2.19e-9 | 3.70e-10 | 2.22e-15 |

The small positive epsilon value at `kappa_bar=100` is below the Phase 2/3 numerical monotonicity tolerance (`1e-9`) and occurs in a stratum where the normalized penalty itself is extremely small. No substantive off-grid violation was observed.

These checks strengthen the evidence that the monotonic patterns are not artifacts of the regular grid. They do not constitute an analytic monotonicity proof.

## 2. Boundary convergence

The Phase 3 guideline used the minimum sampled `tau` that retained at least 99% of the homogeneous contraction margin at `epsilon=0.95`.

Phase 4 adds a bisection reference and compares increasingly dense uniform `tau` grids.

### `kappa_bar = 2`

Bisection reference:

```text
tau* = 0.4076217486520454
```

Grid estimates:

```text
96 points   -> 0.410000
191 points  -> 0.410000
381 points  -> 0.410000
761 points  -> 0.408750
1521 points -> 0.408125
```

### `kappa_bar = 10`

Bisection reference:

```text
tau* = 0.17985615951449502
```

All tested grids from 96 through 1521 points report `0.18` to the displayed precision.

### `kappa_bar = 100`

The entire audited domain `tau >= 0.05` already retains at least 99% of the homogeneous contraction margin at `epsilon=0.95`; therefore no interior boundary occurs inside the study domain.

This convergence study shows that the Phase 3 headline thresholds (`~0.41`, `~0.18`, full studied domain) are stable with respect to grid refinement.

## 3. Wolfram symbolic cross-check

Wolfram Language `15.0.1 for Linux x86 (64-bit) (July 2, 2026)` was used as an independent symbolic engine.

### Scale invariance

Under simultaneous scaling

```text
L -> c L
mu_bar -> c mu_bar
```

Wolfram simplifies the differences in both cubic heterogeneity invariants to

```text
{K1_scaled - K1, K2_scaled - K2} = {0, 0}.
```

At `tau = 1`, it independently recovers

```text
K1 = K2 = ((L - mu_bar)/(L + mu_bar))^2.
```

### Discriminant structure

For each fixed conditioning stratum `kappa_bar in {2, 10, 100}`, let

```text
s = sqrt(epsilon),  0 < s < 1.
```

Wolfram factors the cubic discriminant into a positive rational denominator, the factor

```text
(1 - s)^6 s^4,
```

and a bivariate polynomial in `(s, tau)`.

For all three tested strata, every coefficient of that remaining polynomial is strictly positive:

| `kappa_bar` | coefficient count | minimum coefficient |
| ---: | ---: | ---: |
| 2 | 63 | 1,728 |
| 10 | 63 | 15,718,843,800,000 |
| 100 | 63 | 1,287,108,790,123,562,505,000,000,000 |

Therefore, for each of these three fixed conditioning strata,

```text
0 < s < 1, tau > 0  =>  discriminant > 0.
```

Because the cubic has real coefficients, a strictly positive cubic discriminant implies three distinct real roots. Thus, on the open controlled domain for each tested stratum, the empirical-law cubic has no root-collision boundary.

This is an analytic symbolic result for the three fixed conditioning strata. It is **not** claimed for arbitrary `kappa_bar` without an additional proof.

## 4. Interpretation

Phase 4 separates three levels of evidence:

1. **Dense-grid evidence** from Phases 2/3.
2. **Random off-grid computational robustness** for monotonicity and retention thresholds.
3. **Analytic symbolic structure** for scale invariance and discriminant positivity at the three fixed conditioning strata.

The combination is stronger than increasing grid size alone while keeping the project within the intended computational-stability scope.

## Guardrail

Empirical Law 4.3 itself remains an inherited empirical law. Phase 4 does not prove that its largest admissible root is the universally tight EF21 contraction factor. The new analytic statement concerns the root structure of the inherited cubic on the controlled parameter path, not a new global convergence theorem.
