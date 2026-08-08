# Research Design

## Objective

Characterize how two-agent curvature heterogeneity and communication compression jointly affect the EF21 empirical optimal contraction factor while holding average conditioning fixed.

## Why the controlled parameterization matters

A naive path such as fixing `mu1` and setting `mu2 = tau * mu1` changes both heterogeneity and the average strong-convexity level. Any observed slowdown would then mix two effects:

1. genuine agent heterogeneity, and
2. worsening average conditioning.

To isolate heterogeneity, this project holds

```text
(mu1 + mu2)/2 = mu_bar
```

constant and defines

```text
tau = mu2 / mu1,  0 < tau <= 1.
```

Therefore

```text
mu1 = 2 mu_bar / (1 + tau)
mu2 = 2 mu_bar tau / (1 + tau).
```

At `tau = 1`, the system is homogeneous. As `tau` decreases, the two workers become increasingly heterogeneous without changing the average strong convexity.

## Primary normalized setting

```text
n = 2
L1 = L2 = 1
mu_bar = 0.1
kappa_bar = L / mu_bar = 10
tau in [0.05, 1]
epsilon in [0.01, 0.95]
```

Scale invariance is checked explicitly in the test suite.

## Outcomes

### Optimal empirical contraction factor

For every parameter cell, compute the largest admissible real root `rho_star` of the cubic expression stated in Empirical Law 4.3.

### Homogeneous theoretical baseline

At the same `epsilon`, `L`, and `mu_bar`, compute the homogeneous contraction rate from Theorem 3.1. This is the baseline `rho_homogeneous`.

### Heterogeneity penalty

```text
H_abs = rho_star - rho_homogeneous
```

Because lower contraction factors are better, positive `H_abs` means heterogeneity worsens the predicted rate.

A normalized version is also reported:

```text
H_norm = (rho_star - rho_homogeneous) / (1 - rho_homogeneous)
```

which expresses the penalty relative to the remaining contraction margin.

## Research questions

- **RQ1:** How does `rho_star` change as heterogeneity increases at fixed compression?
- **RQ2:** How does compression sensitivity change across heterogeneity levels?
- **RQ3:** Do heterogeneity and compression exhibit an interaction in the contraction landscape?
- **RQ4:** Which parameter regions produce slow or near-unit contraction?
- **RQ5:** How large is the heterogeneity penalty relative to the homogeneous theoretical baseline?
- **RQ6:** Are the patterns robust across fixed average condition-number strata?

## Planned conditioning strata

The primary landscape uses `kappa_bar = 10`. Robustness analyses will repeat the same experiment at selected strata, initially:

```text
kappa_bar in {2, 10, 100}
```

with `L = 1` and `mu_bar = 1/kappa_bar`.

This treats average conditioning as a controlled scenario variable rather than allowing it to drift with heterogeneity.

## Guardrails

- This repository does **not** claim to prove Empirical Law 4.3.
- Numerical findings will be described as characterization of the empirical cubic law unless an additional proof or certificate is established later.
- Parameter sweeps must retain the homogeneous-limit and scale-invariance regression tests.
- Any practical guideline must be supported by held-out or denser parameter checks rather than inferred from a single coarse visualization.
