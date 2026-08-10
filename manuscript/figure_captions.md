# Figure captions

## Figure 1 — Controlled EF21 contraction landscape

**Figure 1. Optimal contraction factor across heterogeneity and compression at fixed average conditioning.** The surface is evaluated from the inherited two-agent cubic law at `kappa_bar=10`, with `tau=mu2/mu1` controlling worker heterogeneity while `(mu1+mu2)/2` is held fixed. Smaller `tau` corresponds to stronger heterogeneity and larger `epsilon` to heavier compression error. The figure visualizes the joint variation of the largest admissible real root `rho_star`; values closer to one indicate slower linear contraction. The plot is a computational characterization of Empirical Law 4.3 on the audited domain, not a new convergence theorem.

## Figure 2 — Normalized heterogeneity penalty

**Figure 2. Relative loss of contraction margin caused by heterogeneity at `kappa_bar=10`.** The normalized heterogeneity penalty is defined as `H_norm=(rho_star-rho_homogeneous)/(1-rho_homogeneous)`, where `rho_homogeneous` is the homogeneous theoretical baseline evaluated at the same average conditioning and compression level. This normalization expresses the heterogeneous slowdown as a fraction of the contraction margin remaining under the homogeneous baseline and avoids understating differences when both rates are close to one.

## Figure 3 — Compression × conditioning interaction

**Figure 3. Compression amplifies the relative heterogeneity burden, with the magnitude depending on baseline conditioning.** Curves show the normalized heterogeneity penalty versus compression error at the strongest audited heterogeneity (`tau=0.05`) for `kappa_bar in {2,10,100}`. From `epsilon=0.01` to `0.95`, the normalized penalty increases by approximately 3.84x, 3.12x, and 3.03x for `kappa_bar=2,10,100`, respectively. The smaller relative penalty at `kappa_bar=100` should not be interpreted as faster convergence because that stratum is already close to the non-contractive limit over much of the audited domain.

## Figure 4 — 99% contraction-margin retention boundary

**Figure 4. Minimum heterogeneity ratio required to retain 99% of the homogeneous contraction margin.** For each compression level and conditioning stratum, the boundary reports the smallest audited `tau` satisfying `R=(1-rho_star)/(1-rho_homogeneous)>=0.99`. Larger minimum `tau` means that less heterogeneity can be tolerated while preserving the chosen relative margin. At `epsilon=0.95`, continuous bisection references are `tau*=0.4076217487` for `kappa_bar=2` and `tau*=0.1798561595` for `kappa_bar=10`; the full audited range `tau>=0.05` satisfies the 99% criterion for `kappa_bar=100`. These are operating boundaries for the inherited cubic law within the audited domain, not universal stability thresholds.

## Figure 5 — Boundary convergence under grid refinement

**Figure 5. Stability of the 99% retention boundary under increasing `tau`-grid resolution.** Finite-grid estimates at `epsilon=0.95` are compared with bisection references for the three conditioning strata. The grid-derived thresholds converge toward the continuous references as resolution increases, supporting the interpretation that the Phase 3 operating boundaries are not artifacts of a coarse parameter grid. The bisection procedure still evaluates the inherited cubic numerically and therefore does not constitute an analytic convergence proof.

## Figure 6 — Full-regularity mismatch geometry

**Figure 6. Full-regularity mismatch geometry at fixed average conditioning.** The heatmap shows the exact inherited coefficient gap `K1-K2` over the two-dimensional ratio plane `(tau_L,tau_mu)` for `kappa_bar=10`. The dashed diagonal `tau_L=tau_mu` is the proportional-heterogeneity path and forms an exact zero-mismatch valley. Cells violating the local regularity condition `mu_i<=L_i` are masked rather than assigned artificial values. The figure visualizes the controlled fixed-average factorization of the inherited Empirical Law 4.3 coefficients; it does not introduce a separate convergence law.

## Figure 7 — Full-regularity contraction penalty

**Figure 7. Full-regularity normalized contraction penalty under heavy compression.** The heatmap shows the normalized penalty `(rho_star-rho_homogeneous)/(1-rho_homogeneous)` at `kappa_bar=10` and `epsilon=0.95` across `(tau_L,tau_mu)`. The aligned diagonal `tau_L=tau_mu` forms a zero-penalty valley because the inherited cubic reduces exactly to the homogeneous controlled cubic on that path. Moving away from the diagonal activates the nonnegative mismatch coordinate and worsens the inherited largest-root contraction prediction. Invalid local regularity cells remain masked.

## Figure 8 — Rate collapse onto the mismatch coordinate

**Figure 8. Collapse of two-dimensional regularity heterogeneity onto the single mismatch coordinate.** For `epsilon=0.95` and `kappa_bar in {2,10,100}`, every admissible `(tau_L,tau_mu)` pair is plotted as normalized contraction penalty versus `K1-K2`. Within each conditioning stratum, the two-dimensional ratio pairs collapse onto a one-dimensional curve because `K2` and the inherited empirical step size are fixed, while the cubic varies only through `K1=K2+(K1-K2)`. The monotone direction is consistent with the conditional analytic result `d rho_star/dK1>0`. This visualization characterizes the inherited empirical cubic and is not an independent proof of Empirical Law 4.3.

## Figure S1 — Symbolic cubic root structure

**Figure S1. Independent symbolic audit of the inherited cubic discriminant.** For each fixed conditioning stratum `kappa_bar in {2,10,100}`, Wolfram Language factors the discriminant into a positive rational prefactor, `(1-s)^6 s^4`, and a bivariate polynomial `P(s,tau)` whose 63 coefficients are strictly positive. Hence, for `0<s=sqrt(epsilon)<1` and `tau>0`, the discriminant is strictly positive and the cubic has three distinct real roots throughout each audited fixed-conditioning open domain. This result characterizes the root structure of the inherited cubic; it does not prove that Empirical Law 4.3 is a general convergence theorem.

## Table 1 — Key numerical outcomes

**Table 1. Summary of the controlled EF21 sensitivity analysis by average-conditioning stratum.** The table reports the observed range of `rho_star`, maximum absolute and normalized heterogeneity penalties on the dense 216,027-cell grid, the continuous 99% retention boundary at `epsilon=0.95`, and whether the full audited range `tau>=0.05` satisfies the 99% criterion. Values are regenerated from the same analysis code used for the manuscript figures.
