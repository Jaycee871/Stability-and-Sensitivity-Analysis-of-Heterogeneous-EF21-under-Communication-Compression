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

## Phase 2 status

The controlled landscape has now been evaluated at

```text
kappa_bar in {2, 10, 100}
96 tau values x 95 epsilon values x 3 strata = 27,360 cells
```

First computational findings:

1. **Stronger heterogeneity increases the normalized contraction penalty** throughout all three sampled conditioning strata.
2. **Compression amplifies the relative heterogeneity penalty** on the sampled grid: normalized penalty is nondecreasing with `epsilon` within numerical tolerance.
3. **The relative penalty is largest in the better-conditioned stratum.** At `tau=0.05, epsilon=0.95`, the normalized penalties are approximately 5.07% (`kappa_bar=2`), 1.70% (`kappa_bar=10`), and 0.20% (`kappa_bar=100`).
4. **Absolute and normalized penalties peak in different compression regimes.** Absolute gaps peak around `epsilon=0.07--0.11`, whereas normalized penalties peak at the highest studied compression level, `epsilon=0.95`.

These are numerical characterizations of Empirical Law 4.3, not claims of a new theorem. See `docs/phase2_findings.md` and `results/phase2_summary.json` for the audited results and interpretation guardrails.

## Primary outcomes

For each `(tau, epsilon)` cell we compute:

- empirical optimal step size `eta_star`,
- cubic-law contraction factor `rho_star`,
- homogeneous Theorem 3.1 baseline at the same `L` and `mu_bar`,
- absolute heterogeneity penalty,
- normalized heterogeneity penalty relative to the remaining contraction margin.

## Minimal reproducible run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m unittest discover -s tests -v
python scripts/run_grid.py --output outputs/stability_grid.csv
python scripts/analyze_phase2.py
```

The Phase 2 runner writes numerical summaries and three SVG figures under `outputs/phase2/` and `figures/phase2/`.

## Research questions

1. `tau -> rho_star`: heterogeneity sensitivity at fixed compression levels.
2. `epsilon -> rho_star`: compression sensitivity at fixed heterogeneity levels.
3. `(tau, epsilon) -> rho_star`: stability landscape.
4. Heterogeneity penalty relative to the homogeneous theoretical baseline.
5. Interaction between heterogeneity, compression, and average conditioning.
6. Robustness of observed monotonic patterns under denser and off-grid validation.
7. Practical parameter-selection regions, only after robustness checks.

## Provenance

This project extends the independent reproduction repository:

- https://github.com/Jaycee871/-26468-A-Tight-Theory-of-Error-Feedback-Algorithms-in-Distributed-Optimization

The inherited cubic expression is treated as an **empirical law to characterize computationally**, not as a newly proved theorem in this repository.
