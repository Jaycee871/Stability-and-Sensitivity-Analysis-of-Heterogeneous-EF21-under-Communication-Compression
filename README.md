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

## Phase 5 status

The research scope is now locked and the project has entered manuscript assembly. `manuscript/draft.md` contains the first complete paper skeleton, while `scripts/build_paper_assets.py` regenerates the main journal figures and key-results table directly from the audited analysis code.

The paper-asset build produces:

```text
Figure 1  contraction landscape
Figure 2  normalized heterogeneity penalty
Figure 3  compression x conditioning interaction
Figure 4  99% contraction-margin retention boundary
Figure 5  boundary convergence under grid refinement
Figure S1 symbolic root-structure summary
Table 1   key results by conditioning stratum
```

Run

```bash
python scripts/build_paper_assets.py
```

to regenerate the manuscript assets under `paper_assets/`.

See `docs/phase5_manuscript_plan.md` for the claim discipline, section map, and figure rationale.

## Audited results carried into the manuscript

The dense controlled analysis evaluates

```text
kappa_bar in {2, 10, 100}
381 tau values x 189 epsilon values x 3 strata = 216,027 cells
```

and Phase 4 adds deterministic off-grid robustness, boundary-convergence checks, and an independent Wolfram symbolic audit.

### Main findings

1. **Stronger heterogeneity increases the normalized contraction penalty** throughout all three studied conditioning strata.
2. **Compression amplifies the relative heterogeneity burden.** At `tau=0.05`, moving from `epsilon=0.01` to `0.95` multiplies the normalized penalty by about 3.84x (`kappa_bar=2`), 3.12x (`kappa_bar=10`), and 3.03x (`kappa_bar=100`).
3. **The smaller heterogeneity penalty at poor conditioning does not imply better convergence.** In the `kappa_bar=100` dense grid, every cell has `rho_star >= 0.95` and about 63.5% have `rho_star >= 0.99`.
4. **The 99% contraction-margin guideline is stable under grid refinement.** At `epsilon=0.95`, bisection gives

```text
kappa_bar=2  : tau* ~= 0.4076217487
kappa_bar=10 : tau* ~= 0.1798561595
kappa_bar=100: the full audited tau >= 0.05 domain satisfies the target
```

5. **Random off-grid checks support the same monotonic patterns.** Phase 4 evaluates 20,000 deterministic paired samples per conditioning stratum inside the audited domain. No substantive monotonicity violation is observed, and cubic-root residuals remain near machine precision (`~2e-15`).
6. **Wolfram reveals analytic root structure for the three fixed conditioning strata.** For `kappa_bar in {2,10,100}`, the factored cubic discriminant is a positive prefactor times a bivariate polynomial in `s=sqrt(epsilon)` and `tau` whose 63 coefficients are all strictly positive. Therefore the discriminant is positive for `0<s<1`, `tau>0`, and the inherited empirical-law cubic has three distinct real roots throughout each tested open controlled domain.

The off-grid monotonicity and retention statements remain computational claims on the audited domain. The discriminant sign result is analytic only for the three fixed conditioning strata and is not promoted to a general convergence theorem.

See `docs/phase2_findings.md`, `docs/phase3_findings.md`, `docs/phase4_findings.md`, `docs/phase5_manuscript_plan.md`, and the corresponding JSON summaries under `results/`.

## Optional Wolfram symbolic bridge

The Python implementation remains the reproducibility baseline. The Wolfram Language layer under `wolfram/` provides an independent engine for:

- symbolic simplification of the controlled cubic,
- scale-invariance and homogeneous-limit checks,
- discriminant factorization,
- independent numerical roots and retention values,
- restricted Wolfram Cloud API queries.

The shared cases in `wolfram/reference_cases.json` can be evaluated by Wolfram and then cross-checked against Python:

```bash
wolframscript -file wolfram/export_reference.wl
python scripts/compare_wolfram_reference.py wolfram/outputs/wolfram_reference.json
```

Phase 4's symbolic root-structure audit is encoded in `wolfram/phase4_discriminant_checks.wl`.

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
python scripts/analyze_phase4.py
python scripts/build_paper_assets.py
```

## Research questions

1. `tau -> rho_star`: heterogeneity sensitivity at fixed compression levels.
2. `epsilon -> rho_star`: compression sensitivity at fixed heterogeneity levels.
3. `(tau, epsilon) -> rho_star`: stability landscape.
4. Heterogeneity penalty relative to the homogeneous theoretical baseline.
5. Interaction between heterogeneity, compression, and average conditioning.
6. How much homogeneous contraction margin is retained across the parameter landscape?
7. Are the numerical thresholds robust off-grid and under grid refinement?
8. What symbolic structure of the inherited cubic can be certified without claiming a full proof of Empirical Law 4.3?

## Provenance

This project extends the independent reproduction repository:

- https://github.com/Jaycee871/-26468-A-Tight-Theory-of-Error-Feedback-Algorithms-in-Distributed-Optimization

The inherited cubic expression is treated as an **empirical law to characterize computationally**, not as a newly proved theorem in this repository.
