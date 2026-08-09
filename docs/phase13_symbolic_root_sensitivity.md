# Phase 13 — Symbolic Root Structure and Mismatch Sensitivity

## Purpose

Phase 12 reduced full two-agent regularity heterogeneity to a single active cubic-shape gap, `K1-K2`, under fixed arithmetic means. Phase 13 asks whether the numerical sign pattern of the selected largest root can be promoted to an analytic statement **conditional on the inherited Empirical Law 4.3 cubic**.

The answer is yes on the generic controlled domain used by this project.

This phase does **not** prove Empirical Law 4.3 as an EF21 convergence theorem. It proves algebraic and root-structure consequences of that inherited cubic once the cubic is accepted as the object being characterized.

## 1. Shape-coordinate domain inherited from positive local regularity

Let

\[
q_i=\frac{L_i-\mu_i}{L_i+\mu_i},
\qquad
w_i=\frac{L_i+\mu_i}{\sum_j(L_j+\mu_j)}.
\]

For positive admissible local regularity,

\[
0<\mu_i\le L_i,
\]

we have

\[
0\le q_i<1.
\]

Phase 12 established

\[
K_1=\sum_i w_iq_i^2,
\qquad
K_2=\left(\sum_i w_iq_i\right)^2.
\]

Therefore

\[
0\le K_2\le K_1<1.
\]

For the present study, `kappa_bar>1`, so

\[
K_2=\left(\frac{\bar\kappa-1}{\bar\kappa+1}\right)^2>0.
\]

The generic symbolic root audit can therefore use

\[
0<s<1,
\qquad
0<K_2<1,
\qquad
K_2\le K_1<1,
\]

where

\[
s=\sqrt{\epsilon}.
\]

## 2. Inherited cubic

Write

\[
r=\frac{(1-s)^2}{1+s}.
\]

The inherited two-agent cubic is

\[
Q(\rho)=
\rho^3
-\left[s(2+s)+r(sK_1+K_2)\right]\rho^2
+s^2\left[1+2s+r(K_1+sK_2)\right]\rho
-s^4.
\]

The Python implementation remains the numerical baseline. Phase 13 evaluates the generic symbolic statements independently in Wolfram Language.

## 3. Wolfram certificate: the discriminant is strictly positive

Wolfram `Reduce` was asked whether any point satisfying

\[
0<s<1,
\quad
0<K_2<1,
\quad
K_2\le K_1<1
\]

can also satisfy

\[
\operatorname{Disc}_\rho Q\le 0.
\]

The exact result is

```text
False
```

for feasibility of that joint system.

Hence

\[
\operatorname{Disc}_\rho Q>0
\]

throughout the generic shape-coordinate domain. The inherited cubic therefore has three distinct real roots throughout that domain.

This is stronger than the Phase 4 result, which established positive discriminant only after substituting the three fixed equal-smoothness conditioning strata. Phase 13 operates directly in the generic `(s,K1,K2)` coordinate domain.

## 4. All three roots lie in `(0,1)`

Two additional exact `Reduce` checks return `False`:

```text
exists rho <= 0 with Q(rho)=0
exists rho >= 1 with Q(rho)=0
```

under the same shape-coordinate assumptions.

Since the discriminant is positive, all three roots are real and distinct; the two exclusion results place all three roots strictly inside

\[
(0,1).
\]

The nonpositive-root exclusion also has an elementary sign interpretation: for `rho<0`, every term of the cubic is negative because all coefficient groups multiplying the alternating powers are positive.

## 5. The selected largest root lies above `s`

Direct factorization gives

\[
Q(s)=K_2(s-1)^3s^2.
\]

For

\[
0<s<1,
\qquad
K_2>0,
\]

this is strictly negative.

Wolfram also proves that the system

\[
Q(1)\le 0
\]

is infeasible under the generic shape-coordinate assumptions, so

\[
Q(1)>0.
\]

By continuity, at least one root lies in

\[
(s,1).
\]

Since all roots lie in `(0,1)`, the largest real root necessarily satisfies

\[
\rho^\star>s.
\]

## 6. Exact implicit derivative with respect to `K1`

Differentiating the cubic gives

\[
\frac{\partial Q}{\partial K_1}
=-\frac{(1-s)^2}{1+s}\,s\rho(\rho-s).
\]

At a simple root,

\[
\frac{d\rho}{dK_1}
=-\frac{\partial Q/\partial K_1}{\partial Q/\partial\rho}
=
\frac{(1-s)^2}{1+s}
\frac{s\rho(\rho-s)}{Q'(\rho)}.
\]

For a monic cubic with three ordered simple real roots

\[
\rho_1<\rho_2<\rho_3,
\]

we have

\[
Q'(\rho_3)
=(\rho_3-\rho_1)(\rho_3-\rho_2)>0.
\]

The selected root in Empirical Law 4.3 is the largest real root, so

\[
Q'(\rho^\star)>0.
\]

Together with

\[
0<s<\rho^\star<1,
\]

all factors in the derivative are positive. Therefore

\[
\boxed{\frac{d\rho^\star}{dK_1}>0}.
\]

This upgrades the Phase 12 dense-grid observation to an analytic property of the inherited cubic over the generic shape-coordinate domain.

## 7. Consequence for regularity mismatch

Phase 12 proved

\[
K_1-K_2
=\frac{4\bar\kappa^2(\tau_L-\tau_\mu)^2}
{(\bar\kappa+1)^2
(\tau_L+\bar\kappa\tau_\mu+\bar\kappa+1)
(\bar\kappa\tau_L\tau_\mu+\tau_L\tau_\mu+\bar\kappa\tau_L+\tau_\mu)}.
\]

Every denominator factor is positive on the positive controlled domain. Hence

\[
K_1\ge K_2,
\]

with equality exactly when

\[
\tau_L=\tau_\mu.
\]

At fixed average conditioning and compression, `K2` is invariant. Since the selected largest root is strictly increasing in `K1`, the inherited predicted contraction factor is minimized at the minimum possible `K1`, namely

\[
K_1=K_2.
\]

Thus the aligned proportional-heterogeneity path

\[
\tau_L=\tau_\mu
\]

minimizes the inherited largest-root contraction factor over the admissible controlled surface.

Because the aligned path reproduces the homogeneous controlled cubic, the inherited full-heterogeneity penalty relative to that baseline is nonnegative:

\[
\rho^\star(\tau_L,\tau_\mu)
\ge
\rho_{\mathrm{aligned}},
\]

with equality exactly on the aligned path.

This is a statement about the inherited cubic, not a newly proved general EF21 convergence theorem.

## 8. Why this matters scientifically

Phase 11 initially appeared to introduce two independent regularity-heterogeneity axes. Phase 12 showed that the cubic actually sees a fixed `K2` plus a nonnegative mismatch gap `K1-K2`. Phase 13 now shows that the selected inherited contraction factor is strictly increasing in that active shape coordinate.

The resulting structural interpretation is:

> Under fixed average conditioning, the inherited two-agent Empirical Law 4.3 is insensitive to proportional regularity heterogeneity and strictly penalizes regularity-shape mismatch through `K1`.

That statement is substantially sharper than the earlier finite-grid monotonicity observation.

## 9. Reproducibility

The exact Wolfram commands are stored in

```text
wolfram/phase13_full_structure_proof.wl
```

and the evaluated certificate is recorded in

```text
results/phase13_symbolic_certificate.json
```

The certificate records the exact infeasibility results for nonpositive discriminant, nonpositive roots, roots at or above one, and nonpositive `Q(1)`, together with the factorized derivative identities.

## 10. Next step: targeted literature novelty audit

The mathematical object is now precise enough for a focused literature search. The next search should not ask broadly whether heterogeneous distributed optimization exists. It should ask whether prior work has already identified any of the following:

- `K1-K2` as a weighted variance of local condition-shape ratios;
- invariance under aligned proportional smoothness/strong-convexity heterogeneity;
- a mismatch coordinate based on different heterogeneity ratios for `L_i` and `mu_i`;
- monotonic worsening of the inherited EF21 empirical cubic largest root with that mismatch coordinate;
- an equivalent generic discriminant/root-structure characterization in `(s,K1,K2)` coordinates.

This is the appropriate point for the Undermind literature audit.

## Claim guardrail

Phase 13 proves conditional analytic properties of the inherited two-agent Empirical Law 4.3 cubic under the stated controlled assumptions. It does **not** prove the empirical law itself, does **not** establish a new method-agnostic EF21 convergence theorem, and does **not** justify extrapolation to arbitrary `n`, stochastic objectives, or unconstrained heterogeneous regularity without additional proof.
