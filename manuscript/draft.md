# Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression

**Working manuscript draft — Phase 6**

> Status: structured manuscript draft with core literature citations, audited numerical statements, and explicit claim guardrails. Bibliography source: `manuscript/references.bib`.

## Abstract

Error-feedback methods permit communication-efficient distributed optimization under lossy compression, but the interaction between compression and heterogeneous local curvature remains difficult to characterize. The recent work *A Tight Theory of Error Feedback Algorithms in Distributed Optimization* introduced an empirical cubic convergence law for the two-agent heterogeneous setting [@thomsen2026tight]. Building on an independent reproduction of that result, this study performs a controlled stability and sensitivity analysis of the inherited cubic law while holding average conditioning fixed. We parameterize heterogeneity by the ratio `tau = mu2 / mu1` and compression by the contraction error `epsilon`, with `n=2`, `L1=L2=1`, and fixed average strong convexity. Across three average-conditioning strata (`kappa_bar = 2, 10, 100`), a dense 216,027-cell analysis shows that stronger heterogeneity increases the normalized contraction penalty and that heavier compression amplifies this relative burden. At `epsilon=0.95`, retaining at least 99% of the homogeneous contraction margin requires approximately `tau >= 0.4076` for `kappa_bar=2` and `tau >= 0.1799` for `kappa_bar=10`, while the full audited domain `tau>=0.05` satisfies the same relative criterion for `kappa_bar=100`. This apparent robustness at poor conditioning is not faster convergence: all audited `kappa_bar=100` cells are already in a slow-convergence regime. Deterministic off-grid stress tests support the numerical trends, and an independent Wolfram symbolic audit shows that, for each of the three fixed conditioning strata, the cubic discriminant is strictly positive on the open controlled domain, implying three distinct real roots and excluding root-collision transitions there. The resulting characterization converts a reproduced empirical law into an interpretable map of heterogeneity–compression interactions, operating boundaries, and numerical robustness without claiming a general convergence theorem.

## 1. Introduction

Communication is a major bottleneck in large-scale distributed optimization, motivating aggressive quantization and sparsification of worker updates. Error feedback originated as a practical mechanism for carrying compression residuals across iterations and was later given theoretical convergence guarantees for compressed stochastic optimization [@seide2014onebit; @stich2018sparsified; @karimireddy2019error].

EF21 provided a redesigned error-feedback mechanism with distributed convergence guarantees under standard assumptions and contractive compression, including heterogeneous-data settings [@richtarik2021ef21]. More recently, Thomsen, Taylor, and Dieuleveut developed tight rate analyses for classic Error Feedback and EF21, including optimal step sizes and Lyapunov constructions, while explicitly separating proved statements from empirical laws in technically harder heterogeneous regimes [@thomsen2026tight]. Their Empirical Law 4.3 describes the optimal two-agent heterogeneous contraction factor as the largest admissible real root of a cubic polynomial.

The source analysis is closely connected to the performance-estimation-program framework, which formulates worst-case first-order method analysis as an optimization problem and can yield tight semidefinite characterizations [@drori2014performance; @taylor2017exact]. In the reproduced source work, performance estimation and numerical evidence support the heterogeneous cubic law, but a general analytic proof is not supplied [@thomsen2026tight].

The present work does not attempt to prove the full heterogeneous empirical law. Instead, it asks a narrower computational question:

> **How do agent heterogeneity and communication compression jointly affect the inherited optimal contraction factor when average conditioning is held fixed?**

This controlled design is important because changing one worker's strong-convexity parameter alone would simultaneously increase heterogeneity and alter the average conditioning of the optimization problem. We therefore vary the ratio between worker curvatures while holding their average strong convexity constant. This isolates the sensitivity to heterogeneity from changes in baseline problem difficulty.

The study makes four scoped contributions:

1. It introduces a fixed-average two-agent parameterization that separates heterogeneity from average conditioning.
2. It maps the contraction and normalized heterogeneity-penalty landscapes over compression and heterogeneity for three conditioning strata.
3. It converts the landscape into an interpretable contraction-margin-retention guideline and validates the resulting boundaries under grid refinement and deterministic off-grid sampling.
4. It adds an independent symbolic root-structure audit showing a strictly positive cubic discriminant on the three fixed-conditioning open domains studied here.

These contributions are intended as a numerical and mathematical characterization of the inherited empirical law, not as a proof of a general EF21 convergence theorem.

## 2. Background and inherited cubic law

### 2.1 Distributed objective and communication compression

Consider a finite-sum distributed objective

`f(x) = (1/n) sum_i f_i(x)`

with a central server and local workers. Each local function is characterized by a smoothness constant `L_i` and strong-convexity constant `mu_i`. Communication is compressed by a contractive operator with error level `epsilon in (0,1)`, consistent with the contractive-compression setting used in EF21 and the reproduced source paper [@richtarik2021ef21; @thomsen2026tight].

### 2.2 Two-agent heterogeneous empirical law

For `n=2`, Empirical Law 4.3 of the reproduced source paper expresses the optimal contraction factor `rho_star` as the largest admissible real root of [@thomsen2026tight]

`Q(rho) = rho^3 - A rho^2 + B rho - s^4`,

where `s = sqrt(epsilon)`,

`r(s) = (1-s)^2/(1+s)`,

`A = s(2+s) + r(s)(s K1 + K2)`,

`B = s^2[1 + 2s + r(s)(K1 + s K2)]`,

and

`K1 = (Delta2^2 Sigma1 + Delta1^2 Sigma2) / [Sigma1 Sigma2 (Sigma1 + Sigma2)]`,

`K2 = (Delta1 + Delta2)^2 / (Sigma1 + Sigma2)^2`,

with `Sigma_i = L_i + mu_i` and `Delta_i = L_i - mu_i`.

The inherited empirical optimal step size for two workers is

`eta_star = 4 / [(L1+mu1)+(L2+mu2)] * (1-s)/(1+s)`.

The present paper treats these expressions as inherited objects to characterize computationally and symbolically.

## 3. Methods

### 3.1 Controlled heterogeneity path

We set

`n = 2`, `L1 = L2 = L = 1`,

and define the average strong convexity

`mu_bar = (mu1 + mu2)/2`.

Heterogeneity is parameterized by

`tau = mu2 / mu1`, `0 < tau <= 1`.

Holding `mu_bar` fixed gives

`mu1 = 2 mu_bar/(1+tau)`,

`mu2 = 2 mu_bar tau/(1+tau)`.

Thus, varying `tau` changes worker heterogeneity while preserving average strong convexity. `tau=1` is homogeneous, while smaller `tau` corresponds to stronger heterogeneity.

### 3.2 Conditioning strata

With `L=1`, we use

`kappa_bar = L/mu_bar`

and study

`kappa_bar in {2, 10, 100}`.

These strata represent progressively harder average conditioning while keeping the heterogeneity mechanism identical.

### 3.3 Primary outcomes

For each `(tau, epsilon, kappa_bar)` configuration, the analysis computes:

- inherited empirical optimal step size `eta_star`;
- largest admissible real cubic root `rho_star`;
- homogeneous Theorem 3.1 baseline `rho_homogeneous` at the same `L`, `mu_bar`, and `epsilon` [@thomsen2026tight];
- absolute heterogeneity penalty

  `H_abs = rho_star - rho_homogeneous`;

- normalized heterogeneity penalty

  `H_norm = (rho_star - rho_homogeneous)/(1-rho_homogeneous)`;

- contraction-margin retention

  `R = (1-rho_star)/(1-rho_homogeneous) = 1-H_norm`.

The normalized quantity prevents a small absolute difference near `rho=1` from being misread as negligible when the remaining contraction margin is itself very small.

### 3.4 Dense parameter study

The primary dense analysis uses

- `tau in [0.05,1]`, 381 evenly spaced points;
- `epsilon in [0.01,0.95]`, 189 evenly spaced points;
- three conditioning strata.

This yields

`381 x 189 x 3 = 216,027`

controlled configurations.

### 3.5 Retention boundaries

For a target retention `R0`, a one-sided operating boundary is defined as the smallest studied `tau` satisfying

`R(tau, epsilon, kappa_bar) >= R0`.

The main guideline uses `R0=0.99`. Grid-based boundaries are complemented by bisection references at `epsilon=0.95` to quantify grid-resolution error.

### 3.6 Off-grid robustness

Phase 4 evaluates 20,000 deterministic random paired checks per conditioning stratum within the audited domain. Each paired check tests whether the observed ordering with respect to `tau` or `epsilon` persists at points not present on the regular grid. The same audit records the residual of the selected cubic root under the original polynomial.

These tests are numerical stress tests, not proofs of global monotonicity.

### 3.7 Independent symbolic audit

A separate Wolfram Language implementation independently reconstructs the controlled cubic. The symbolic layer is used to verify scale invariance, the homogeneous reduction, and the sign structure of the cubic discriminant. Python remains the primary reproducibility pipeline.

For each fixed `kappa_bar in {2,10,100}`, Wolfram factors the discriminant into a positive rational prefactor, `(1-s)^6 s^4`, and a bivariate polynomial in `(s,tau)` whose 63 coefficients are all strictly positive. Therefore, for `0<s<1` and `tau>0`, the discriminant is strictly positive in each of the three audited fixed-conditioning open domains.

## 4. Results

### 4.1 Contraction landscape

**Figure 1** maps `rho_star(tau, epsilon)` for `kappa_bar=10`. Convergence becomes slower as compression error increases, and the heterogeneous surface separates from the homogeneous edge as `tau` decreases.

**Figure file:** `paper_assets/figures/figure1_contraction_landscape.svg`

### 4.2 Relative heterogeneity penalty

**Figure 2** maps `H_norm` for the same conditioning stratum. Across the audited grid, stronger heterogeneity increases the normalized penalty. The relative burden also increases with heavier compression within numerical tolerance.

**Figure file:** `paper_assets/figures/figure2_normalized_penalty.svg`

Across the dense grid, the maximum normalized penalties are approximately:

- `5.07%` for `kappa_bar=2`;
- `1.70%` for `kappa_bar=10`;
- `0.20%` for `kappa_bar=100`.

### 4.3 Compression–conditioning interaction

At the maximum studied heterogeneity `tau=0.05`, increasing `epsilon` from `0.01` to `0.95` multiplies the normalized penalty by approximately:

- `3.84x` for `kappa_bar=2`;
- `3.12x` for `kappa_bar=10`;
- `3.03x` for `kappa_bar=100`.

**Figure 3** shows this interaction directly.

The smaller relative penalty at poor conditioning must not be interpreted as better convergence. In the `kappa_bar=100` dense study, every cell has `rho_star >= 0.95`, and roughly 63.5% have `rho_star >= 0.99`. The baseline is therefore already close to the non-contractive limit, leaving less relative margin for heterogeneity to consume.

**Figure file:** `paper_assets/figures/figure3_conditioning_interaction.svg`

### 4.4 Contraction-margin operating boundaries

**Figure 4** converts the normalized penalty into a 99% retention boundary. At the heaviest audited compression level `epsilon=0.95`, bisection gives

- `tau_star = 0.4076217486520454` for `kappa_bar=2`;
- `tau_star = 0.17985615951449502` for `kappa_bar=10`;
- the entire audited range `tau>=0.05` for `kappa_bar=100`.

These are operating thresholds for the inherited cubic law within the audited domain, not universal convergence thresholds.

**Figure file:** `paper_assets/figures/figure4_retention_boundary.svg`

### 4.5 Boundary robustness

**Figure 5** compares finite-grid boundary estimates against bisection references as the number of `tau` grid points increases. The Phase 3 headline values (`~0.41`, `~0.18`, and full-domain satisfaction) remain stable through refinement to 1521 grid points.

**Figure file:** `paper_assets/figures/figure5_boundary_convergence.svg`

The deterministic off-grid audit similarly finds no substantive monotonicity violation under the project's `1e-9` numerical interpretation tolerance. Maximum root residuals remain at approximately `2e-15`.

### 4.6 Symbolic root structure

The symbolic audit provides a complementary structural result. For each fixed conditioning stratum studied here, the discriminant is strictly positive for

`0 < s = sqrt(epsilon) < 1`, `tau > 0`.

Consequently, the inherited cubic has three distinct real roots throughout each audited open controlled domain. Root collision is therefore not responsible for the numerical sensitivity patterns observed in Figures 1–4.

**Supplementary figure:** `paper_assets/figures/figureS1_symbolic_root_structure.svg`

## 5. Discussion

The controlled analysis separates three effects that are easily confounded in heterogeneous distributed optimization: average conditioning, local curvature imbalance, and compression strength. Holding average strong convexity fixed reveals that the heterogeneous penalty is not merely a consequence of changing the average condition number.

The normalized penalty is particularly useful for interpretation. Absolute differences in contraction factor can become small near `rho=1`, even though the same difference represents a meaningful fraction of the remaining contraction margin. This explains why the `kappa_bar=100` stratum can display a small normalized heterogeneity effect while still being the slowest regime in absolute terms.

The retention formulation also converts an abstract cubic root into an operating guideline. Instead of asking only whether heterogeneity worsens the rate, practitioners can ask how much of the homogeneous contraction margin they are willing to lose and identify compatible `(tau, epsilon)` regions.

The positive-discriminant result narrows the interpretation further. Within the three fixed conditioning strata, the sensitivity landscape does not arise from changes in the number of real cubic roots or root collisions. The dominant root moves continuously through a three-real-root regime. This analytic observation is deliberately narrower than a proof of the empirical convergence law but strengthens the numerical characterization.

## 6. Limitations

1. The study characterizes an inherited empirical cubic law; it does not prove Empirical Law 4.3 in full generality [@thomsen2026tight].
2. The main parameterization fixes `n=2` and `L1=L2=1`.
3. Numerical monotonicity statements are restricted to the audited domain `tau in [0.05,1]` and `epsilon in [0.01,0.95]`.
4. The symbolic discriminant statement is currently established only for the three fixed conditioning strata `kappa_bar in {2,10,100}`.
5. The retention boundary is a rate-based guideline, not a direct communication-cost optimum.
6. Empirical behavior on large stochastic machine-learning tasks is outside the present scope and should not be inferred from the cubic characterization alone.

## 7. Conclusion

This study extends a reproduced two-agent heterogeneous EF21 result by replacing a collection of validation points with a controlled stability and sensitivity characterization. Fixing average conditioning isolates the effect of heterogeneity, while normalized contraction penalties and margin-retention boundaries provide interpretable measures of its interaction with communication compression. Dense-grid, off-grid, boundary-refinement, and independent symbolic checks produce a consistent picture: stronger heterogeneity consumes contraction margin, heavier compression amplifies the relative burden, and the cubic remains in a three-distinct-real-root regime across the three audited fixed-conditioning domains. The result is a scoped computational and mathematical extension that remains reproducible without claiming a general convergence theorem.

## Figure and table map

- **Figure 1:** contraction landscape — `figure1_contraction_landscape.svg`
- **Figure 2:** normalized heterogeneity penalty — `figure2_normalized_penalty.svg`
- **Figure 3:** compression × conditioning interaction — `figure3_conditioning_interaction.svg`
- **Figure 4:** 99% retention operating boundary — `figure4_retention_boundary.svg`
- **Figure 5:** boundary convergence under grid refinement — `figure5_boundary_convergence.svg`
- **Figure S1:** symbolic root-structure note — `figureS1_symbolic_root_structure.svg`
- **Table 1:** key results by conditioning stratum — `table1_key_results.csv`

Full publication-style captions are maintained in `manuscript/figure_captions.md`.

## References

Bibliographic metadata and citation keys are maintained in `manuscript/references.bib`.
