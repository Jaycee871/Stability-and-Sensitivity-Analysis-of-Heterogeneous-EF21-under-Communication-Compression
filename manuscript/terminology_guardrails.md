# Manuscript Terminology Guardrails

These definitions prevent a scoped computational/symbolic characterization from being read as a broader theorem.

## Stability analysis

In this manuscript, **stability analysis** means analysis of the robustness and sensitivity of the inherited contraction-rate characterization under changes in heterogeneity and compression. It includes:

- variation of the admissible contraction factor `rho_star`;
- loss and retention of homogeneous contraction margin;
- stability of numerical operating boundaries under grid refinement;
- off-grid robustness checks;
- root-multiplicity structure of the inherited cubic.

It does **not** mean that the manuscript establishes a new Lyapunov-stability, asymptotic-stability, or global convergence theorem for EF21.

## Operating boundary

A **retention operating boundary** is a parameter-selection boundary induced by a chosen contraction-margin criterion such as 99% retention. It is conditional on the inherited cubic, audited conditioning stratum, and parameter domain.

It is not a universal stability threshold, feasibility boundary, or communication-complexity lower bound.

## Monotonicity

The manuscript may state that a quantity is monotone **on the audited grid** or that deterministic off-grid checks **support the same ordering within numerical tolerance**.

It must not state global analytic monotonicity unless a separate proof is added.

## Symbolic result

The positive-discriminant result is an **analytic root-structure statement for the fixed strata `kappa_bar in {2,10,100}`**. It establishes three distinct real roots of the inherited cubic on the tested open controlled domains.

It does not establish that the cubic itself is the true convergence law outside the status already assigned to Empirical Law 4.3 by the source paper.

## Robustness

When referring to `kappa_bar=100`, avoid saying the method is “more robust” merely because the normalized heterogeneity penalty is smaller. The baseline contraction factor is already close to one. Prefer:

> “The incremental heterogeneity penalty is smaller relative to a baseline that is already slow.”

## Recommended novelty sentence

> “The novelty of this study lies not in re-deriving the inherited cubic law, but in converting it into a controlled fixed-average sensitivity map, contraction-margin operating guidelines, off-grid and grid-resolution robustness checks, and a fixed-stratum symbolic characterization of its root structure.”
