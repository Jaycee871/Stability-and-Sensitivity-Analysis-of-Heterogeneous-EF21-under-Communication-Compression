# Stability and Sensitivity Analysis of Heterogeneous EF21 under Communication Compression

**Working manuscript draft — Phase 20**

> Status: full-regularity manuscript and publication-figure integration with audited numerical, algebraic, symbolic, and primary-source evidence. Bibliography source: `manuscript/references.bib`. Empirical Law 4.3, its cubic, and its coefficients are inherited from Thomsen, Taylor, and Dieuleveut; this manuscript analyzes that inherited object and does not present it as a newly proved EF21 convergence theorem.

## Abstract

Error-feedback methods permit communication-efficient distributed optimization under lossy compression, yet the interaction between communication error and heterogeneous local regularity can be difficult to interpret from convergence formulas alone. Thomsen, Taylor, and Dieuleveut recently proposed Empirical Law 4.3 for the two-agent heterogeneous EF21 setting, in which the predicted optimal contraction factor is the largest real root of a cubic polynomial [@thomsen2026tight]. Building on an independent reproduction, we first isolate strong-convexity heterogeneity at fixed average conditioning and map its interaction with compression across `216,027` controlled configurations. We then generalize the controlled design by allowing both local smoothness and local strong convexity to vary independently while fixing their arithmetic means. In this full-regularity parameterization, the inherited empirical step size and the cubic coordinate `K2` are invariant. The difference `K1-K2` admits the exact inherited interpretation of a weighted variance of local condition-shape ratios, and under the fixed-average parameterization it further factors explicitly with `(tau_L-tau_mu)^2` as its unique mismatch factor. Consequently, proportional smoothness/strong-convexity heterogeneity (`tau_L=tau_mu`) leaves the inherited cubic unchanged, whereas mismatch activates a nonnegative structural penalty coordinate. A generic symbolic audit of the inherited cubic establishes three distinct real roots in `(0,1)`, locates the selected largest root above `sqrt(epsilon)`, and yields positive implicit sensitivity `d rho_star/dK1 > 0`. Conditional on Empirical Law 4.3, regularity mismatch therefore strictly worsens the predicted largest-root contraction factor. These results convert an inherited empirical cubic from a numerical rate formula into an interpretable stability and sensitivity structure while preserving a strict distinction between analysis of the empirical law and proof of EF21 convergence.

## 1. Introduction

Communication is a major bottleneck in large-scale distributed optimization, motivating quantization, sparsification, and other compressed-update schemes. Error feedback carries compression residuals across iterations and can recover useful convergence behavior despite biased or lossy communication [@seide2014onebit; @stich2018sparsified; @karimireddy2019error]. EF21 redesigned this mechanism and established distributed convergence guarantees under standard assumptions and contractive compression [@richtarik2021ef21].

The literature contains several distinct meanings of heterogeneity. Statistical or data heterogeneity concerns differences in local data distributions or stochastic gradients. Regularity heterogeneity concerns differences in local smoothness or convexity constants. These distinctions matter because a method can accommodate heterogeneous data without analyzing a family of local strong-convexity constants. For example, later EF21-related work has sharpened dependence on heterogeneous smoothness constants and introduced smoothness-dependent weighting [@richtarik2024reloaded], while EControl allows local smoothness constants but places strong convexity on the averaged objective rather than requiring a separate local strong-convexity constant for every worker [@gao2023econtrol].

Thomsen, Taylor, and Dieuleveut developed tight analyses of classic Error Feedback and EF21 and explicitly separated proved results from empirical laws in more difficult heterogeneous regimes [@thomsen2026tight]. Their Empirical Law 4.3 addresses the two-agent case with heterogeneous local regularity parameters and expresses the predicted optimal contraction factor as the largest real root of a cubic polynomial. The source analysis is closely connected to the performance-estimation-program framework, in which worst-case first-order method analysis can be cast as semidefinite optimization [@drori2014performance; @taylor2017exact]. Agent-symmetry reductions in related PEP work also show why two-agent cases can be structurally informative in distributed performance analysis, although for different algorithms and assumptions [@colla2024symmetries].

The present work does not attempt to prove the full heterogeneous empirical law. Instead, it asks two nested questions:

> **How do local regularity heterogeneity and communication compression jointly affect the inherited EF21 contraction prediction when average conditioning is held fixed?**

and, after both smoothness and strong convexity are allowed to vary,

> **Can the apparent two-dimensional heterogeneity dependence be reduced to a smaller structural coordinate that explains when heterogeneity is harmful and when it is invisible to the inherited cubic?**

The study makes six scoped contributions.

1. We reproduce the two-agent inherited cubic and construct a fixed-average equal-smoothness baseline that isolates strong-convexity heterogeneity from changes in average conditioning.
2. We map the compression–heterogeneity interaction over `216,027` baseline configurations, derive contraction-margin-retention guidelines, and stress-test the numerical patterns off-grid and under boundary refinement.
3. We extend the controlled design to simultaneous smoothness and strong-convexity heterogeneity using independent ratios `tau_L=L2/L1` and `tau_mu=mu2/mu1`, while fixing both arithmetic means and explicitly masking invalid local regularity cells.
4. We distinguish an inherited algebraic interpretation from the controlled structural contribution: `K1-K2` is exactly a weighted variance of inherited local condition-shape coordinates, while the fixed-average parameterization yields an explicit rational factorization whose mismatch dependence is carried by `(tau_L-tau_mu)^2`.
5. We show that proportional regularity heterogeneity, `tau_L=tau_mu`, leaves the inherited cubic unchanged at fixed average conditioning and compression, even when both workers remain heterogeneous in their raw `L_i` and `mu_i` values.
6. Conditional on the inherited Empirical Law 4.3 cubic, we establish a generic root-location and sensitivity result: all three roots lie in `(0,1)`, the largest root exceeds `sqrt(epsilon)`, and `d rho_star/dK1>0`, so any admissible nonzero mismatch strictly worsens the predicted contraction factor.

These are scoped statements about an inherited empirical object. The manuscript does not claim that the cubic, `K1`, `K2`, polynomial root-location techniques, or the underlying EF21 convergence law are newly derived here.

## 2. Background and inherited cubic law

### 2.1 Distributed objective and communication compression

Consider the finite-sum distributed objective

\[
f(x)=\frac{1}{n}\sum_{i=1}^{n} f_i(x),
\]

with a central server and local workers. Worker `i` is associated with a smoothness constant `L_i` and, in the heterogeneous strongly convex setting studied by the inherited empirical law, a local strong-convexity constant `mu_i`. Communication is compressed by a contractive operator with error level `epsilon in (0,1)`, consistent with the EF21 setting and the reproduced source paper [@richtarik2021ef21; @thomsen2026tight].

### 2.2 Two-agent heterogeneous Empirical Law 4.3

For `n=2`, define

\[
\Sigma_i=L_i+\mu_i,\qquad \Delta_i=L_i-\mu_i,
\]

and

\[
K_1=
\frac{\Delta_2^2\Sigma_1+\Delta_1^2\Sigma_2}
{\Sigma_1\Sigma_2(\Sigma_1+\Sigma_2)},
\qquad
K_2=
\left(\frac{\Delta_1+\Delta_2}{\Sigma_1+\Sigma_2}\right)^2.
\]

Let

\[
s=\sqrt{\epsilon},
\qquad
r(s)=\frac{(1-s)^2}{1+s}.
\]

Empirical Law 4.3 expresses the predicted optimal contraction factor `rho_star` as the largest real root of [@thomsen2026tight]

\[
Q(\rho)=\rho^3-A\rho^2+B\rho-s^4,
\]

where

\[
A=s(2+s)+r(s)(sK_1+K_2),
\]

\[
B=s^2\left[1+2s+r(s)(K_1+sK_2)\right].
\]

The inherited empirical optimal step size is

\[
\eta^\star=
\frac{4}{(L_1+\mu_1)+(L_2+\mu_2)}
\frac{1-s}{1+s}.
\]

The present manuscript treats these expressions as inherited objects. The purpose of the analysis is to expose their controlled sensitivity structure, not to promote Empirical Law 4.3 into a general theorem.

### 2.3 Nearby heterogeneity analyses

Prior EF21 work already contains meaningful treatments of heterogeneity, but the relevant axes differ. Error Feedback Reloaded improves dependence on heterogeneous smoothness constants from a quadratic-mean quantity to an arithmetic-mean quantity and uses smoothness-aware weighting [@richtarik2024reloaded]. This makes broad statements such as “variance-style heterogeneity has not been studied in EF21” inappropriate. However, its regularity descriptor is built from smoothness heterogeneity rather than the paired local `(L_i,mu_i)` condition-shape mismatch studied below.

EControl is another important near neighbor. It allows worker-dependent smoothness constants but imposes strong convexity on the average objective with a single global parameter, while individual local objectives need not be strongly convex [@gao2023econtrol]. Thus its heterogeneity model does not instantiate the simultaneous local `(L_i,mu_i)` structure required by the present controlled mismatch coordinate. These distinctions motivate precise claim wording rather than broad absence-of-prior-work statements.

## 3. Methods

### 3.1 Equal-smoothness baseline

The baseline controlled path sets

\[
n=2,\qquad L_1=L_2=L=1,
\]

and fixes the average strong convexity

\[
\bar\mu=\frac{\mu_1+\mu_2}{2}.
\]

Strong-convexity heterogeneity is parameterized by

\[
\tau=\frac{\mu_2}{\mu_1},\qquad 0<\tau\le 1.
\]

Holding `mu_bar` fixed gives

\[
\mu_1=\frac{2\bar\mu}{1+\tau},
\qquad
\mu_2=\frac{2\bar\mu\tau}{1+\tau}.
\]

Thus, varying `tau` changes local strong-convexity imbalance without changing average strong convexity. The homogeneous case is `tau=1`.

### 3.2 Conditioning strata and baseline outcomes

With `L=1`, define

\[
\bar\kappa=\frac{L}{\bar\mu}.
\]

The baseline studies `kappa_bar in {2,10,100}`. For each `(tau,epsilon,kappa_bar)` cell, the analysis records the inherited empirical step size, the selected largest real root `rho_star`, the homogeneous Theorem 3.1 baseline `rho_homogeneous`, the absolute penalty

\[
H_{\rm abs}=\rho^\star-\rho_{\rm homogeneous},
\]

the normalized penalty

\[
H_{\rm norm}=\frac{\rho^\star-\rho_{\rm homogeneous}}
{1-\rho_{\rm homogeneous}},
\]

and contraction-margin retention

\[
R=\frac{1-\rho^\star}{1-\rho_{\rm homogeneous}}=1-H_{\rm norm}.
\]

The normalized quantity avoids interpreting a small absolute difference near `rho=1` as negligible when the remaining contraction margin is itself small.

### 3.3 Baseline dense study and retention boundaries

The primary baseline grid uses

- `tau in [0.05,1]`, 381 evenly spaced points;
- `epsilon in [0.01,0.95]`, 189 evenly spaced points;
- `kappa_bar in {2,10,100}`.

This yields

\[
381\times 189\times 3=216{,}027
\]

controlled configurations.

For a target retention `R0`, the one-sided operating boundary is the smallest studied `tau` satisfying

\[
R(\tau,\epsilon,\bar\kappa)\ge R_0.
\]

The main guideline uses `R0=0.99`; finite-grid estimates are compared with bisection references at `epsilon=0.95`.

### 3.4 Baseline off-grid robustness

The Phase 4 stress test evaluates 20,000 deterministic paired off-grid samples per conditioning stratum. Each comparison checks whether the numerical ordering with respect to `tau` or `epsilon` agrees with the dense-grid pattern, and the original cubic residual of each selected root is recorded. These tests are numerical stress tests, not proofs of global monotonicity.

### 3.5 Full-regularity fixed-average parameterization

The full extension releases the equal-smoothness constraint and fixes both arithmetic means:

\[
\bar L=\frac{L_1+L_2}{2},
\qquad
\bar\mu=\frac{\mu_1+\mu_2}{2},
\qquad
\bar\kappa=\frac{\bar L}{\bar\mu}.
\]

Smoothness and strong-convexity heterogeneity are varied independently through

\[
\tau_L=\frac{L_2}{L_1},
\qquad
\tau_\mu=\frac{\mu_2}{\mu_1},
\qquad
0<\tau_L,\tau_\mu\le 1.
\]

The controlled reconstruction is

\[
L_1=\frac{2\bar L}{1+\tau_L},
\qquad
L_2=\tau_L L_1,
\]

\[
\mu_1=\frac{2\bar\mu}{1+\tau_\mu},
\qquad
\mu_2=\tau_\mu\mu_1.
\]

A cell is admissible only if `0<mu_i<=L_i` for both workers. Invalid local regularity combinations are masked rather than coerced into the domain.

The default full-regularity audit uses 31 values for each heterogeneity ratio, 95 compression values, and three conditioning strata:

\[
31\times31\times95\times3=273{,}885
\]

requested cells, of which `258,400` satisfy the local regularity constraints.

### 3.6 Inherited weighted-moment interpretation

Define the local condition-shape coordinate

\[
q_i=\frac{L_i-\mu_i}{L_i+\mu_i}=\frac{\Delta_i}{\Sigma_i}
\]

and weights

\[
w_i=\frac{\Sigma_i}{\Sigma_1+\Sigma_2}.
\]

Direct substitution into the inherited definitions gives

\[
K_1=\sum_i w_iq_i^2,
\qquad
K_2=\left(\sum_iw_iq_i\right)^2,
\]

and therefore

\[
K_1-K_2=\operatorname{Var}_w(q_i).
\]

This identity is an exact algebraic reinterpretation of the inherited coefficients, not a separate theorem-level contribution. Its role is to expose the meaning of the coefficient difference before the controlled parameterization is applied.

### 3.7 Fixed-average mismatch factorization

Because both arithmetic means are fixed, the inherited empirical step size is constant over `(tau_L,tau_mu)` at fixed `(L_bar,mu_bar,epsilon)`. The same controlled path also gives the exact invariant

\[
K_2=\left(\frac{\bar\kappa-1}{\bar\kappa+1}\right)^2.
\]

The remaining regularity dependence is carried by `K1-K2`. Algebraic simplification yields

\[
K_1-K_2=
\frac{4\bar\kappa^2(\tau_L-\tau_\mu)^2}
{(\bar\kappa+1)^2
(\tau_L+\bar\kappa\tau_\mu+\bar\kappa+1)
(\bar\kappa\tau_L\tau_\mu+\tau_L\tau_\mu+\bar\kappa\tau_L+\tau_\mu)}.
\]

Every denominator factor is positive on the admissible positive domain. Hence

\[
K_1\ge K_2,
\]

with equality exactly when

\[
\tau_L=\tau_\mu.
\]

This aligned path represents proportional local regularity scaling: each worker can remain heterogeneous in raw `L_i` and `mu_i`, but the smoothness and strong-convexity ratios change in lockstep.

### 3.8 Generic symbolic root and sensitivity audit

The full-regularity structure motivates a cubic-coordinate analysis independent of any particular `(tau_L,tau_mu)` grid. For the studied `kappa_bar>1` setting, positivity of the local regularity parameters and the weighted-moment representation imply

\[
0<K_2\le K_1<1,
\qquad
0<s<1.
\]

A separate Wolfram Language proof script analyzes the inherited cubic on this generic domain. The symbolic certificate establishes that the discriminant is strictly positive, excludes roots at or below zero and at or above one, and evaluates

\[
Q(s)=K_2(s-1)^3s^2<0.
\]

Thus all three roots are distinct and lie in `(0,1)`, while the selected largest root satisfies

\[
\rho^\star>s=\sqrt\epsilon.
\]

Implicit differentiation with respect to `K1` gives

\[
\frac{d\rho^\star}{dK_1}
=
\frac{(1-s)^2}{1+s}
\frac{s\rho^\star(\rho^\star-s)}{Q'(\rho^\star)}.
\]

At the largest simple real root, `Q'(rho_star)>0`. Therefore

\[
\frac{d\rho^\star}{dK_1}>0.
\]

This is a conditional statement about the inherited cubic. It does not prove that Empirical Law 4.3 itself is the true EF21 convergence law for all heterogeneous problems.

## 4. Results

### 4.1 Equal-smoothness contraction landscape

Figure 1 maps `rho_star(tau,epsilon)` for `kappa_bar=10`. Convergence becomes slower as compression error increases, and the heterogeneous surface separates from the homogeneous edge as `tau` decreases.

**Figure file:** `paper_assets/figures/figure1_contraction_landscape.svg`

### 4.2 Relative heterogeneity penalty

Figure 2 maps `H_norm` for the same conditioning stratum. Across the audited baseline grid, stronger strong-convexity heterogeneity increases the normalized penalty, and the relative burden increases with heavier compression within numerical tolerance.

Across the dense grid, the maximum normalized penalties are approximately:

- `5.07%` for `kappa_bar=2`;
- `1.70%` for `kappa_bar=10`;
- `0.20%` for `kappa_bar=100`.

**Figure file:** `paper_assets/figures/figure2_normalized_penalty.svg`

### 4.3 Compression–conditioning interaction

At the strongest audited baseline heterogeneity, `tau=0.05`, increasing `epsilon` from `0.01` to `0.95` multiplies the normalized penalty by approximately:

- `3.84x` for `kappa_bar=2`;
- `3.12x` for `kappa_bar=10`;
- `3.03x` for `kappa_bar=100`.

The smaller relative penalty at poor conditioning must not be interpreted as faster convergence. In the `kappa_bar=100` dense study, every cell has `rho_star>=0.95`, and roughly `63.5%` have `rho_star>=0.99`. The baseline is already close to the non-contractive limit, leaving less relative margin for heterogeneity to consume.

**Figure file:** `paper_assets/figures/figure3_conditioning_interaction.svg`

### 4.4 Contraction-margin operating boundaries

Figure 4 converts the normalized penalty into a 99% retention boundary. At `epsilon=0.95`, bisection gives

- `tau_star=0.4076217486520454` for `kappa_bar=2`;
- `tau_star=0.17985615951449502` for `kappa_bar=10`;
- full-domain satisfaction for the audited range `tau>=0.05` when `kappa_bar=100`.

These are operating thresholds for the inherited cubic within the audited domain, not universal convergence thresholds.

**Figure file:** `paper_assets/figures/figure4_retention_boundary.svg`

### 4.5 Boundary and off-grid robustness

Figure 5 compares finite-grid boundary estimates with bisection references as the number of `tau` grid points increases. The headline values remain stable through refinement to 1521 grid points. The deterministic off-grid audit likewise finds no substantive ordering violation under the project's `1e-9` numerical interpretation tolerance, while maximum cubic-root residuals remain approximately `2e-15`.

**Figure file:** `paper_assets/figures/figure5_boundary_convergence.svg`

### 4.6 Fixed-stratum symbolic audit

The Phase 4 symbolic audit independently factors the discriminant for each `kappa_bar in {2,10,100}` into a positive rational prefactor, `(1-s)^6s^4`, and a bivariate polynomial in `(s,tau)` whose 63 coefficients are strictly positive. Therefore the inherited cubic has three distinct real roots throughout each of those open equal-smoothness controlled domains.

This fixed-stratum factorization is only for the three fixed conditioning strata. It is retained as an independent audit even though the later Phase 13 certificate supplies a more general cubic-coordinate root result.

**Supplementary figure:** `paper_assets/figures/figureS1_symbolic_root_structure.svg`

### 4.7 Full-regularity heterogeneity reduces to a mismatch coordinate

Once both `L_i` and `mu_i` vary while their arithmetic means remain fixed, neither the inherited empirical step size nor `K2` changes across the controlled heterogeneity surface. Consequently, the apparent two-dimensional dependence enters the cubic through the single nonnegative gap `K1-K2`.

The weighted-variance identity explains the geometry of this gap: it measures dispersion of the local condition-shape coordinates `q_i`, rather than raw dispersion of `L_i` or `mu_i` alone. The full dense audit requested `273,885` configurations and retained `258,400` admissible cells after enforcing `mu_i<=L_i`. Across all admissible cells, the exact moment identity, invariant `K2`, and fixed-average rational factorization reproduce to machine precision.

**Figure file:** `paper_assets/phase19_full_regularity/figure6_mismatch_geometry.svg`

### 4.8 Proportional heterogeneity is invisible to the inherited cubic

The explicit factorization contains `(tau_L-tau_mu)^2` and no other zero-producing numerator factor on the positive admissible domain. Therefore `tau_L=tau_mu` is exactly the zero-mismatch path.

Along this path, both workers may have different smoothness constants and different strong-convexity constants. Nevertheless, their regularity pairs are scaled proportionally, `K1=K2`, the inherited step size remains fixed, and the cubic coefficients coincide with those of the homogeneous controlled case at the same `kappa_bar` and `epsilon`.

This separates **heterogeneity magnitude** from **regularity mismatch**. Heterogeneity by itself need not activate a penalty in the inherited empirical law; disagreement between the smoothness and strong-convexity heterogeneity ratios does.

**Figure file:** `paper_assets/phase19_full_regularity/figure7_full_regularity_penalty.svg`

### 4.9 Regularity mismatch strictly worsens the inherited largest-root prediction

The generic symbolic certificate shows that the inherited cubic has three distinct roots in `(0,1)` on the cubic-coordinate domain `0<s<1`, `0<K2<=K1<1`. Because the selected largest root lies above `s` and is a simple root, the implicit derivative satisfies

\[
\frac{d\rho^\star}{dK_1}>0.
\]

At fixed average conditioning and compression, `K2` is invariant while `K1=K2+(K1-K2)`. Combining this sensitivity with the nonnegative mismatch factorization yields the conditional ordering

\[
\rho^\star(\tau_L,\tau_\mu)
\ge
\rho^\star(\tau,\tau),
\]

with strict inequality whenever the admissible cell has `tau_L!=tau_mu`.

Thus the aligned path minimizes the inherited largest-root contraction prediction over the controlled full-regularity surface. This conclusion is conditional on Empirical Law 4.3 and should not be read as a separately proved EF21 convergence theorem.

**Figure file:** `paper_assets/phase19_full_regularity/figure8_rate_collapse.svg`

## 5. Discussion

### 5.1 From heterogeneity magnitude to heterogeneity mismatch

The baseline experiment initially suggests a familiar story: more local curvature imbalance is associated with a worse inherited contraction prediction, and stronger compression amplifies the relative burden. The full-regularity extension changes the interpretation. When smoothness and strong convexity are allowed to move independently, the decisive structural quantity is not simply how unequal the workers are. The inherited cubic distinguishes whether the two types of regularity heterogeneity are aligned.

This observation explains why raw parameter heterogeneity can coexist with a homogeneous cubic prediction. On the path `tau_L=tau_mu`, each worker preserves the same local condition-shape coordinate even though its absolute regularity scale differs. The cubic therefore sees no mismatch. Moving off that path creates dispersion in the local condition-shape coordinates and activates `K1-K2`.

### 5.2 What is inherited and what is derived here

The distinction between N1a and N1b is important for interpretation. The identity

\[
K_1-K_2=\operatorname{Var}_w(q_i)
\]

is an exact rewrite of the source paper's inherited coefficients. Its value is explanatory: it reveals that `K1` and `K2` are a weighted second moment and squared weighted mean. The controlled factorization in `(kappa_bar,tau_L,tau_mu)`, by contrast, exposes how that inherited gap behaves under fixed arithmetic means and makes the alignment condition explicit.

The same distinction applies to the root analysis. The cubic is inherited. The symbolic discriminant, root localization, and implicit sensitivity characterize that cubic; they do not replace the source paper's empirical status with a general EF21 theorem.

### 5.3 Relation to prior EF21 heterogeneity analyses

Existing EF21-family analyses already show that heterogeneous smoothness can affect complexity bounds and weighting choices [@richtarik2024reloaded]. The present mismatch coordinate should therefore not be described as the introduction of heterogeneity or variance-style reasoning into EF21. Its narrower role is to characterize the joint local `(L_i,mu_i)` dependence of the inherited two-agent cubic under a fixed-average design.

Likewise, data-heterogeneity and error-control analyses such as EControl address an important but different regime [@gao2023econtrol]. The primary-source audit for this manuscript found that EControl permits local `L_i` but uses a single strong-convexity parameter for the averaged objective, so it does not instantiate the paired local regularity structure analyzed here. The named related-work chain was checked for theorem-level equivalents to the fixed-average factorization, aligned invariance, and inherited-cubic root sensitivity; no equivalent was identified within that named chain. This scoped audit is not a universal absence-of-prior-work claim.

### 5.4 Practical interpretation

The retention formulation remains useful for the equal-smoothness baseline because it translates an abstract contraction factor into a fraction of homogeneous contraction margin retained under heterogeneity. The full-regularity result adds a second interpretation: if local smoothness and strong convexity move proportionally across workers, the inherited cubic predicts no regularity-mismatch penalty at all. If they move differently, the penalty coordinate grows from zero and the selected root worsens monotonically with it.

This does not directly prescribe an optimal distributed learning system, since the model abstracts away many costs and stochastic effects. It does, however, distinguish two types of heterogeneity that would otherwise be conflated in parameter sweeps.

## 6. Limitations

1. The study characterizes an inherited empirical cubic law; it does not prove Empirical Law 4.3 in full generality [@thomsen2026tight].
2. All full-regularity structural conclusions remain restricted to the inherited two-agent (`n=2`) cubic. They should not be generalized to arbitrary numbers of workers without separate analysis.
3. The equal-smoothness numerical monotonicity statements are restricted to `tau in [0.05,1]`, `epsilon in [0.01,0.95]`, and the audited conditioning strata. The off-grid checks are not proofs of global monotonicity.
4. The Phase 4 factorized discriminant statement is only for the three fixed conditioning strata `kappa_bar in {2,10,100}`. Phase 13 provides a separate generic result on the stated `(s,K1,K2)` domain, conditional on the inherited cubic.
5. The full-regularity grid explicitly excludes cells violating `mu_i<=L_i`; conclusions are not extended across invalid local regularity combinations.
6. The contraction-margin boundary is a rate-based guideline, not a direct communication-cost optimum.
7. The primary-source closure establishes that no theorem-level equivalent was identified in the named EF/error-feedback chain inspected for this project. It does not certify universal bibliographic novelty, and absolute claims such as “first” or “no prior work” are intentionally avoided.
8. Empirical behavior on large stochastic machine-learning tasks is outside the present scope and should not be inferred from the cubic characterization alone.

## 7. Conclusion

This study turns a reproduced two-agent heterogeneous EF21 empirical law into a layered stability and sensitivity analysis. The equal-smoothness baseline shows how strong-convexity heterogeneity consumes contraction margin and how communication compression amplifies that relative burden. The full-regularity extension then reveals a sharper structural explanation. At fixed arithmetic-mean regularity, the inherited step size and `K2` are invariant; the remaining coefficient gap is interpretable as a weighted dispersion of local condition-shape coordinates and factors explicitly through the squared mismatch `(tau_L-tau_mu)^2`. Proportional heterogeneity therefore leaves the inherited cubic unchanged, while nonzero regularity mismatch activates the penalty coordinate. A generic symbolic analysis further shows that the inherited largest root increases strictly with that coordinate. The resulting contribution is a controlled computational and mathematical characterization of an inherited empirical object, with numerical, algebraic, symbolic, and literature-audit layers kept explicitly separate from any claim of a general EF21 convergence proof.

## Figure and table map

- **Figure 1:** contraction landscape — `figures/figure1_contraction_landscape.svg`
- **Figure 2:** normalized heterogeneity penalty — `figures/figure2_normalized_penalty.svg`
- **Figure 3:** compression × conditioning interaction — `figures/figure3_conditioning_interaction.svg`
- **Figure 4:** 99% retention operating boundary — `figures/figure4_retention_boundary.svg`
- **Figure 5:** boundary convergence under grid refinement — `figures/figure5_boundary_convergence.svg`
- **Figure 6:** full-regularity mismatch geometry — `phase19_full_regularity/figure6_mismatch_geometry.svg`
- **Figure 7:** full-regularity normalized contraction penalty — `phase19_full_regularity/figure7_full_regularity_penalty.svg`
- **Figure 8:** rate collapse onto `K1-K2` — `phase19_full_regularity/figure8_rate_collapse.svg`
- **Figure S1:** fixed-stratum symbolic root-structure note — `figures/figureS1_symbolic_root_structure.svg`
- **Table 1:** equal-smoothness key results by conditioning stratum — `tables/table1_key_results.csv`

Phase 20 integrates Figures 6–8 into the reproducible paper-asset and MDPI submission pipelines. Full publication-style captions are maintained in `manuscript/figure_captions.md`.

## References

Bibliographic metadata and citation keys are maintained in `manuscript/references.bib`.
