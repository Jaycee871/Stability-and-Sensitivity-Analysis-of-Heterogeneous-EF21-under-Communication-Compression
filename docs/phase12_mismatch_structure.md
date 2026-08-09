# Phase 12 — Regularity-Mismatch Structure

## Why this phase exists

Phase 11 opened the full two-agent regularity surface by varying both smoothness and strong-convexity heterogeneity at fixed arithmetic means. Phase 12 asks a sharper question:

> Does the inherited Empirical Law 4.3 actually depend on two independent heterogeneity coordinates, or can the surface be reduced to a smaller structural quantity?

The answer is unexpectedly clean. Under the controlled fixed-average parameterization, the empirical step size is invariant, `K2` is invariant, and all regularity-shape variation enters the inherited cubic through the single nonnegative gap `K1-K2`.

## 1. Controlled coordinates

Let

\[
\bar L=\frac{L_1+L_2}{2},\qquad
\bar\mu=\frac{\mu_1+\mu_2}{2},\qquad
\bar\kappa=\frac{\bar L}{\bar\mu},
\]

and

\[
\tau_L=\frac{L_2}{L_1},\qquad
\tau_\mu=\frac{\mu_2}{\mu_1}.
\]

The controlled pairs are

\[
L_1=\frac{2\bar L}{1+\tau_L},\qquad
L_2=\frac{2\bar L\tau_L}{1+\tau_L},
\]

\[
\mu_1=\frac{2\bar\mu}{1+\tau_\mu},\qquad
\mu_2=\frac{2\bar\mu\tau_\mu}{1+\tau_\mu}.
\]

As established in Phase 11, the inherited empirical step size depends on the sum

\[
(L_1+\mu_1)+(L_2+\mu_2)=2(\bar L+\bar\mu),
\]

so it is constant across the `tau_L x tau_mu` surface at fixed average conditioning and compression.

## 2. `K2` is not a heterogeneity coordinate on this controlled surface

Write

\[
\Sigma_i=L_i+\mu_i,\qquad \Delta_i=L_i-\mu_i.
\]

The inherited cubic uses

\[
K_2=\frac{(\Delta_1+\Delta_2)^2}{(\Sigma_1+\Sigma_2)^2}.
\]

Fixed arithmetic means give

\[
\Delta_1+\Delta_2=2(\bar L-\bar\mu),
\]

and

\[
\Sigma_1+\Sigma_2=2(\bar L+\bar\mu).
\]

Therefore

\[
K_2=\left(\frac{\bar L-\bar\mu}{\bar L+\bar\mu}\right)^2
=\left(\frac{\bar\kappa-1}{\bar\kappa+1}\right)^2.
\]

Thus `K2` is completely determined by average conditioning and is independent of both heterogeneity ratios.

## 3. `K1-K2` is a weighted variance

For two agents,

\[
K_1
=\frac{\Delta_1^2/\Sigma_1+\Delta_2^2/\Sigma_2}{\Sigma_1+\Sigma_2}.
\]

Define

\[
q_i=\frac{\Delta_i}{\Sigma_i}
=\frac{L_i-\mu_i}{L_i+\mu_i},
\qquad
w_i=\frac{\Sigma_i}{\Sigma_1+\Sigma_2}.
\]

Then

\[
K_1=w_1q_1^2+w_2q_2^2,
\]

while

\[
K_2=(w_1q_1+w_2q_2)^2.
\]

Hence

\[
K_1-K_2
=w_1(q_1-\bar q)^2+w_2(q_2-\bar q)^2\ge 0,
\]

where `bar q=w1 q1+w2 q2`.

This gives a direct interpretation: **the extra regularity coordinate in the inherited cubic is a weighted dispersion of local condition-shape ratios, not heterogeneity in absolute scale by itself.**

## 4. Exact mismatch formula in `(tau_L,tau_mu)` coordinates

Let

\[
a=\tau_L,\qquad b=\tau_\mu,\qquad k=\bar\kappa.
\]

Direct simplification gives

\[
K_1-K_2=
\frac{4k^2(a-b)^2}
{(k+1)^2(a+bk+k+1)(abk+ab+ak+b)}.
\]

Every denominator factor is positive on the admissible controlled domain. Therefore

\[
K_1\ge K_2,
\]

with equality exactly when

\[
\tau_L=\tau_\mu.
\]

The equality condition has a natural interpretation. When `tau_L=tau_mu`, each worker's `L_i` and `mu_i` are scaled by the same factor, so both workers have the same local condition ratio `L_i/mu_i` even though their absolute regularity scales may be heterogeneous.

## 5. Aligned heterogeneity is empirically invisible to the inherited cubic

Along

\[
\tau_L=\tau_\mu,
\]

we have

\[
K_1=K_2=\left(\frac{\bar\kappa-1}{\bar\kappa+1}\right)^2.
\]

The empirical step size is already invariant, and the cubic coefficients therefore coincide with the homogeneous controlled coefficients at the same `bar kappa` and `epsilon`.

This means that, within the inherited two-agent Empirical Law 4.3 and this fixed-average parameterization, **proportional regularity heterogeneity does not change the predicted optimal contraction factor.** What matters is mismatch between smoothness heterogeneity and strong-convexity heterogeneity.

The dense Phase 12 audit confirms the aligned-path equality to floating-point error only: the maximum absolute `rho_star-rho_homogeneous` discrepancy is below `9e-13` in all three conditioning strata.

## 6. Admissible-domain boundary is analytic

The inherited local regularity requirement is

\[
0<\mu_i\le L_i.
\]

For fixed `tau_L=a` and `k=bar kappa`, the worker-1 constraint gives

\[
\tau_\mu\ge \frac{1+a-k}{k},
\]

intersected with `[0,1]`.

The worker-2 constraint gives, when

\[
1-(k-1)a>0,
\]

\[
\tau_\mu\le \frac{ka}{1-(k-1)a};
\]

otherwise the upper constraint is automatically satisfied over `(0,1]`.

At the audited minimum `tau_L=0.05`, this yields upper bounds

- `0.1052631579` for `bar kappa=2`,
- `0.9090909091` for `bar kappa=10`,
- `1` for `bar kappa=100`.

This exactly explains why the Phase 11 square contains many invalid cells at `bar kappa=2`, only a thin invalid corner at `bar kappa=10`, and no invalid cells at `bar kappa=100` on the chosen `[0.05,1]^2` domain.

## 7. Dense numerical audit

The Phase 12 production audit evaluates the same requested grid as Phase 11:

```text
31 tau_L values x 31 tau_mu values x 95 epsilon values x 3 conditioning strata
= 273,885 requested cells
```

After regularity masking, `258,400` cells are valid.

The exact identities are reproduced to machine precision. Across the dense grid:

- no valid cell has a heterogeneity penalty below `-1e-10`;
- `K2` invariance error is at most about `4.4e-16`;
- the closed-form `K1-K2` identity is accurate to about `4.5e-16`;
- the weighted-variance representation is accurate to about `4.5e-16`;
- every audited cubic discriminant is positive;
- every audited selected root satisfies `rho_star > sqrt(epsilon)`;
- every audited implicit derivative `d rho_star / d K1` is positive.

The maximum normalized penalty on the current grid occurs at `epsilon=0.95` in all three conditioning strata:

- `bar kappa=2`: about `5.0736%`, at `(tau_L,tau_mu)=(1,0.05)`;
- `bar kappa=10`: about `4.7697%`, at the nearest admissible grid point `(0.05,0.905)`;
- `bar kappa=100`: about `1.0152%`, at `(0.05,1)`.

For `bar kappa=10`, the continuous admissibility boundary at `tau_L=0.05` is `tau_mu<=0.9090909`; therefore the dense-grid maximizer at `0.905` is visibly boundary-limited rather than an arbitrary interior point.

## 8. Root sensitivity to the mismatch coordinate

For the inherited cubic `Q(rho)=0`, the partial derivative with respect to `K1` is

\[
\frac{\partial Q}{\partial K_1}
=r s\rho(s-\rho),
\]

where

\[
s=\sqrt{\epsilon},\qquad
r=\frac{(1-s)^2}{1+s}.
\]

At a simple selected root,

\[
\frac{d\rho}{dK_1}
=
\frac{r s\rho(\rho-s)}{Q'(\rho)}.
\]

The dense numerical audit finds positive discriminant, `rho>s`, `Q'(rho)>0`, and therefore positive `d rho/dK1` at every audited valid cell. This strongly supports the computational statement that increasing the mismatch coordinate worsens the inherited contraction factor on the studied domain.

This derivative-sign statement remains a numerical-domain result until the required root-structure conditions are proved for the full admissible parameter domain.

## 9. Scientific interpretation

Phase 11 began with two heterogeneity ratios. Phase 12 shows that, at fixed average conditioning, the inherited cubic sees them in a much more structured way:

1. the empirical step size does not move;
2. `K2` does not move;
3. aligned proportional heterogeneity leaves the cubic unchanged;
4. the nonnegative mismatch quantity `K1-K2` carries the structural deviation;
5. numerically, larger mismatch corresponds to a worse selected contraction factor on the audited domain.

A useful working interpretation is therefore:

> For the inherited two-agent empirical law, **regularity mismatch matters more directly than regularity heterogeneity itself.**

This wording is intentionally restricted to the inherited law and the controlled parameterization.

## 10. Next steps

The next mathematical step is a Wolfram symbolic audit of the Phase 12 identities and the root-sensitivity sign conditions. After that, a targeted literature search should ask whether this exact `K1-K2` weighted-variance interpretation, aligned-heterogeneity invariance, or mismatch-sensitive EF21 characterization has already appeared in distributed-optimization literature.

That literature search is the appropriate point to use Undermind. OSF should remain the final archival layer after the claim set, manuscript, code, and figures are frozen.

## Claim guardrail

Phase 12 does not prove Empirical Law 4.3 itself and does not claim a new general EF21 convergence theorem. The algebraic identities in Sections 2–6 are exact consequences of the inherited two-agent cubic under the controlled parameterization. The global derivative-sign interpretation is currently supported numerically on the audited domain and remains subject to symbolic proof before being elevated to an analytic statement.
