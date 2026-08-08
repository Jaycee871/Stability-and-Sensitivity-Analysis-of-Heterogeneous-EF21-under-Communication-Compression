# Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression

A computational extension of the reproduced two-agent heterogeneous EF21 result from **A Tight Theory of Error Feedback Algorithms in Distributed Optimization** (ICML 2026 paper #26468; Empirical Law 4.3).

## Research question

**How do agent heterogeneity and communication compression jointly affect the optimal contraction rate of EF21 when average conditioning is held fixed?**

The study isolates heterogeneity from average problem difficulty by using

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

so changing `tau` changes heterogeneity while keeping `(mu1 + mu2)/2` constant.

## Phase 3 status

The dense controlled analysis now evaluates

```text
kappa_bar in {2, 10, 100}
381 tau values x 189 epsilon values x 3 strata = 216,027 cells
```

### Main computational findings

1. **Stronger heterogeneity increases the normalized contraction penalty** throughout all three studied conditioning strata.
2. **Compression amplifies the relative heterogeneity burden.** At `tau=0.05`, moving from `epsilon=0.01` to `0.95` multiplies the normalized penalty by about 3.84x (`kappa_bar=2`), 3.12x (`kappa_bar=10`), and 3.03x (`kappa_bar=100`).
3. **The smaller heterogeneity penalty at poor conditioning does not imply better convergence.** In the `kappa_bar=100` dense grid, every cell has `rho_star >= 0.95` and about 63.5% have `rho_star >= 0.99`.
4. **Contraction-margin retention gives an interpretable operating guideline.** Define

```text
R = (1 - rho_star) / (1 - rho_homogeneous)
  = 1 - normalized_penalty.
```

At `epsilon=0.95`, retaining at least 99% of the homogeneous contraction margin requires approximately

```text
kappa_bar=2   : tau >= 0.41
kappa_bar=10  : tau >= 0.18
kappa_bar=100 : all studied tau >= 0.05 satisfy the target
```

These are finite-grid computational boundaries for Empirical Law 4.3, not universal analytic thresholds.

See `docs/phase2_findings.md`, `docs/phase3_findings.md`, `results/phase2_summary.json`, and `results/phase3_summary.json` for the audited findings and interpretation guardrails.

## Optional Wolfram symbolic bridge

The Python implementation remains the reproducibility baseline. An optional Wolfram Language layer under `wolfram/` provides an independent engine for:

- symbolic simplification of the controlled cubic,
- scale-invariance and homogeneous-limit checks,
- discriminant exploration,
- independent numerical roots and retention values,
- restricted Wolfram Cloud API queries.

The shared cases in `wolfram/reference_cases.json` can be evaluated by Wolfram and then cross-checked against Python:

```bash
wolframscript -file wolfram/export_reference.wl
python scripts/compare_wolfram_reference.py wolfram/outputs/wolfram_reference.json
```

The Cloud API template defaults to private access and deliberately exposes no arbitrary Wolfram-expression evaluation. See `wolfram/README.md` for deployment details.

## Primary outcomes

For each `(tau, epsilon)` cell we compute:

- empirical optimal step size `eta_star`,
- cubic-law contraction factor `rho_star`,
- homogeneous Theorem 3.1 baseline at the same `L` and `mu_bar`,
- absolute heterogeneity penalty,
- normalized heterogeneity penalty relative to the remaining contraction margin,
- contraction-margin retention used for practical boundary construction.

## Minimal reproducible run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m unittest discover -s tests -v
python scripts/run_grid.py --output outputs/stability_grid.csv
python scripts/analyze_phase2.py
python scripts/analyze_phase3.py
```

The Phase 2 and Phase 3 runners write numerical summaries, CSV tables, and SVG figures under `outputs/` and `figures/`.

## Research questions

1. `tau -> rho_star`: heterogeneity sensitivity at fixed compression levels.
2. `epsilon -> rho_star`: compression sensitivity at fixed heterogeneity levels.
3. `(tau, epsilon) -> rho_star`: stability landscape.
4. Heterogeneity penalty relative to the homogeneous theoretical baseline.
5. Interaction between heterogeneity, compression, and average conditioning.
6. How much homogeneous contraction margin is retained across the parameter landscape?
7. Which compression levels are compatible with a chosen retention target for an observed heterogeneity ratio?

## Provenance

This project extends the independent reproduction repository:

- https://github.com/Jaycee871/-26468-A-Tight-Theory-of-Error-Feedback-Algorithms-in-Distributed-Optimization

The inherited cubic expression is treated as an **empirical law to characterize computationally**, not as a newly proved theorem in this repository.
