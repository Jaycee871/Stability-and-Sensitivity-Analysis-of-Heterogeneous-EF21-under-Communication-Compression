# Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression

A computational and mathematical extension of the reproduced two-agent heterogeneous EF21 result from **A Tight Theory of Error Feedback Algorithms in Distributed Optimization** (ICML 2026 paper #26468; Empirical Law 4.3).

## Research question

**How do local regularity heterogeneity and communication compression jointly affect the inherited optimal contraction factor of EF21 when average conditioning is held fixed?**

The project contains nested controlled designs and progressively stronger computational/algebraic audits.

### Phases 1–10: equal-smoothness baseline

The original controlled path uses

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

so changing `tau` changes strong-convexity heterogeneity while keeping `(mu1 + mu2)/2` constant.

### Phases 11–13: full regularity heterogeneity

The extension fixes both arithmetic means

```text
L_bar  = (L1 + L2)/2
mu_bar = (mu1 + mu2)/2
kappa_bar = L_bar / mu_bar
```

and varies two ratios independently:

```text
tau_L  = L2/L1
tau_mu = mu2/mu1
```

with

```text
L1  = 2 * L_bar  / (1 + tau_L)
L2  = tau_L  * L1
mu1 = 2 * mu_bar / (1 + tau_mu)
mu2 = tau_mu * mu1
```

Invalid cells violating `mu_i <= L_i` are explicitly masked rather than coerced.

## Phase 12 — regularity mismatch structure

Phase 12 reduces the apparent two-dimensional heterogeneity dependence to a cleaner structural coordinate.

For the inherited Empirical Law 4.3, define

```text
Sigma_i = L_i + mu_i
Delta_i = L_i - mu_i
```

and the cubic shape coordinates `K1` and `K2`. Under the fixed-average Phase 11 parameterization:

1. the empirical step size is invariant across `(tau_L,tau_mu)`;
2. `K2` is exactly invariant and equals

```text
((kappa_bar - 1)/(kappa_bar + 1))^2
```

3. `K1-K2` is a nonnegative weighted variance of

```text
q_i = (L_i - mu_i)/(L_i + mu_i)
```

4. the exact controlled-path mismatch identity is

```text
K1 - K2 =
4*kappa_bar^2*(tau_L-tau_mu)^2 /
[(kappa_bar+1)^2
 * (tau_L+kappa_bar*tau_mu+kappa_bar+1)
 * (kappa_bar*tau_L*tau_mu+tau_L*tau_mu+kappa_bar*tau_L+tau_mu)]
```

Therefore `K1 >= K2`, with equality exactly when `tau_L=tau_mu`.

Along this aligned path, `L_i` and `mu_i` may both be heterogeneous, but the local condition ratios remain aligned. The inherited cubic coefficients then coincide with the homogeneous controlled coefficients at the same average conditioning and compression. In other words, **proportional regularity heterogeneity is invisible to the inherited two-agent cubic; mismatch between smoothness and strong-convexity heterogeneity is the active structural deviation.**

The default Phase 12 dense audit requests

```text
31 tau_L values x 31 tau_mu values x 95 epsilon values x 3 strata
= 273,885 cells
```

of which `258,400` are regularity-admissible. The exact identities reproduce to machine precision.

## Phase 13 — generic symbolic root structure and sensitivity

Phase 13 upgrades the Phase 12 numerical root-sensitivity observation to a conditional analytic statement about the inherited cubic.

Positive local regularity and the weighted-moment representation imply

```text
0 < K2 < 1
K2 <= K1 < 1
0 < s < 1,  s = sqrt(epsilon)
```

for the studied `kappa_bar>1` setting.

Wolfram `Reduce` certifies on this generic `(s,K1,K2)` domain that:

- `Discriminant[Q,rho] <= 0` is infeasible, so the cubic has three distinct real roots;
- `rho <= 0 && Q(rho)==0` is infeasible;
- `rho >= 1 && Q(rho)==0` is infeasible;
- `Q(1) <= 0` is infeasible;
- `Q(s) = K2*(s-1)^3*s^2 < 0`.

Therefore all three roots lie in `(0,1)`, and the selected largest root satisfies

```text
rho_star > s.
```

The exact implicit derivative is

```text
d rho_star / d K1
= ((1-s)^2/(1+s))*s*rho_star*(rho_star-s) / Q'(rho_star)
```

and `Q'(rho_star)>0` at the largest simple root. Hence

```text
d rho_star / d K1 > 0.
```

Combining this with the Phase 12 identity `K1>=K2` proves, **conditional on the inherited Empirical Law 4.3 cubic**, that the controlled predicted contraction factor is minimized on the aligned path `tau_L=tau_mu`; any admissible regularity mismatch with `K1>K2` strictly worsens the inherited largest-root contraction factor.

The Wolfram proof script and evaluated certificate are stored in

```text
wolfram/phase13_full_structure_proof.wl
results/phase13_symbolic_certificate.json
```

See `docs/phase13_symbolic_root_sensitivity.md` for the proof chain and claim guardrail.

## Phase 5 manuscript assets

The equal-smoothness baseline manuscript pipeline remains reproducible. `manuscript/draft.md` contains the current paper skeleton, while `scripts/build_paper_assets.py` regenerates the original main journal figures and key-results table directly from the audited analysis code.

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

The main manuscript has **not yet been rewritten to promote Phase 11–13 findings**. Those findings remain staged until the targeted literature novelty audit is complete.

Run

```bash
python scripts/build_paper_assets.py
```

to regenerate the existing manuscript assets under `paper_assets/`.

## Audited equal-smoothness results carried into the current manuscript

The dense controlled Phase 2–3 analysis evaluates

```text
kappa_bar in {2, 10, 100}
381 tau values x 189 epsilon values x 3 strata = 216,027 cells
```

and Phase 4 adds deterministic off-grid robustness, boundary-convergence checks, and an independent Wolfram symbolic audit.

### Main equal-smoothness findings

1. **Stronger strong-convexity heterogeneity increases the normalized contraction penalty** throughout all three studied conditioning strata.
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

The Phase 13 generic certificate now subsumes the root-reality conclusion at the cubic-coordinate level; the Phase 4 result remains useful as an independent fixed-stratum factorization audit.

## Optional Wolfram symbolic bridge

The Python implementation remains the reproducibility baseline. The Wolfram Language layer under `wolfram/` provides an independent engine for:

- symbolic simplification of the controlled cubic,
- scale-invariance and homogeneous-limit checks,
- discriminant factorization and generic `Reduce` certificates,
- independent numerical roots and retention values,
- restricted Wolfram Cloud API queries.

The shared cases in `wolfram/reference_cases.json` can be evaluated by Wolfram and then cross-checked against Python:

```bash
wolframscript -file wolfram/export_reference.wl
python scripts/compare_wolfram_reference.py wolfram/outputs/wolfram_reference.json
```

Phase 4's fixed-stratum symbolic audit is encoded in `wolfram/phase4_discriminant_checks.wl`. Phase 13's generic root and sensitivity audit is encoded in `wolfram/phase13_full_structure_proof.wl`.

## Primary outcomes

For each controlled cell or analytic coordinate domain we compute or audit:

- empirical optimal step size `eta_star`,
- cubic-law contraction factor `rho_star`,
- homogeneous Theorem 3.1 baseline at the same average regularity,
- absolute and normalized heterogeneity penalties,
- contraction-margin retention,
- full-heterogeneity regularity feasibility,
- inherited cubic coordinates `K1` and `K2`,
- exact mismatch gap `K1-K2`,
- generic cubic discriminant/root-location structure,
- analytic selected-root sensitivity with respect to `K1`.

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
python scripts/analyze_phase11.py
python scripts/analyze_phase12.py
python scripts/build_paper_assets.py

# optional independent symbolic engine
wolframscript -file wolfram/phase13_full_structure_proof.wl
```

## Research questions

1. How does strong-convexity heterogeneity affect the inherited contraction factor at fixed smoothness?
2. How does compression interact with that equal-smoothness heterogeneity burden?
3. How do smoothness and strong-convexity heterogeneity interact when varied independently?
4. Which full-heterogeneity cells are excluded by local regularity `mu_i <= L_i`?
5. Why does aligned proportional heterogeneity leave the inherited cubic unchanged?
6. Can `K1-K2` be interpreted as the sufficient mismatch coordinate at fixed average conditioning?
7. What generic root structure makes the largest-root sensitivity analytically positive?
8. Has an equivalent mismatch/weighted-variance characterization already appeared in distributed-optimization literature?
9. Is the Phase 13 conditional analytic result novel relative to prior EF21/error-feedback theory?
10. Which Phase 11–13 findings should be promoted into the final manuscript after the literature audit?

## Provenance

This project extends the independent reproduction repository:

- https://github.com/Jaycee871/-26468-A-Tight-Theory-of-Error-Feedback-Algorithms-in-Distributed-Optimization

The inherited cubic expression is treated as an **empirical law to characterize computationally and algebraically**, not as a newly proved convergence theorem in this repository.
