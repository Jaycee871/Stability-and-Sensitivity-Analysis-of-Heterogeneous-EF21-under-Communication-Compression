# Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression

A computational extension of the reproduced two-agent heterogeneous EF21 result from **A Tight Theory of Error Feedback Algorithms in Distributed Optimization** (ICML 2026 paper #26468; Empirical Law 4.3).

## Research question

**How do agent heterogeneity and communication compression jointly affect the optimal contraction rate of EF21 when average conditioning is held fixed?**

The key design choice is to isolate heterogeneity from average problem difficulty. We normalize

- `n = 2`,
- `L1 = L2 = L = 1`,
- fixed average strong convexity `mu_bar = (mu1 + mu2)/2`,
- heterogeneity ratio `tau = mu2 / mu1`, with `0 < tau <= 1`,
- compression error `0 < epsilon < 1`.

For fixed `mu_bar`,

```text
mu1 = 2 * mu_bar / (1 + tau)
mu2 = 2 * mu_bar * tau / (1 + tau)
```

so changing `tau` changes heterogeneity while keeping `(mu1 + mu2)/2` constant. This prevents a slower rate caused by worsening average conditioning from being misidentified as a heterogeneity effect.

## Primary outcomes

For each `(tau, epsilon)` cell we compute:

- empirical optimal step size `eta_star`,
- cubic-law contraction factor `rho_star`,
- homogeneous Theorem 3.1 baseline at the same `L` and `mu_bar`,
- absolute heterogeneity penalty,
- normalized heterogeneity penalty relative to the remaining contraction margin.

The initial study uses `mu_bar = 0.1` (`kappa_bar = 10`) and will later repeat the same controlled analysis across selected conditioning strata such as `kappa_bar in {2, 10, 100}`.

## Minimal reproducible run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m unittest discover -s tests -v
python scripts/run_grid.py --output outputs/stability_grid.csv
```

The default grid contains 9,120 cells (`96 tau` values x `95 epsilon` values).

## Planned analyses

1. `tau -> rho_star` heterogeneity sensitivity at fixed compression levels.
2. `epsilon -> rho_star` compression sensitivity at fixed heterogeneity levels.
3. `(tau, epsilon) -> rho_star` stability landscape.
4. Heterogeneity penalty relative to the homogeneous theoretical baseline.
5. Interaction patterns and practical parameter-selection regions.
6. Robustness across fixed average condition-number strata.

## Provenance

This project extends the independent reproduction repository:

- https://github.com/Jaycee871/-26468-A-Tight-Theory-of-Error-Feedback-Algorithms-in-Distributed-Optimization

The inherited cubic expression is treated as an **empirical law to characterize computationally**, not as a newly proved theorem in this repository.
