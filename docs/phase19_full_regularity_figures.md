# Phase 19 — Full-Regularity Publication Figures

## Purpose

Phase 18 integrates the full-regularity structural findings into the manuscript. Phase 19 supplies the visual evidence required to make that structural story immediately legible.

The figure set is deliberately organized around the progression

```text
two heterogeneity ratios -> one mismatch valley -> one rate coordinate
```

rather than adding another collection of generic parameter heatmaps.

## Figure 6 — mismatch geometry

`figure6_mismatch_geometry.svg` plots the exact controlled coordinate

\[
K_1-K_2
\]

over `(tau_L,tau_mu)` for the representative stratum `kappa_bar=10`.

The diagonal `tau_L=tau_mu` is overlaid explicitly. On that line the mismatch coordinate is zero. Invalid local regularity cells remain masked rather than being assigned artificial values.

Interpretation: raw heterogeneity can be large while the inherited mismatch coordinate remains zero if smoothness and strong-convexity heterogeneity are proportionally aligned.

## Figure 7 — full-regularity contraction penalty

`figure7_full_regularity_penalty.svg` maps the normalized contraction penalty at `epsilon=0.95` and `kappa_bar=10` over the same ratio plane.

The aligned diagonal forms a zero-penalty valley because the inherited cubic coincides with its homogeneous controlled counterpart there. Moving away from the diagonal activates the mismatch coordinate and worsens the inherited largest-root prediction.

The visual is a consequence of the inherited empirical law plus the Phase 12/13 structural analysis; it is not an independent EF21 convergence theorem.

## Figure 8 — rate collapse onto K1-K2

`figure8_rate_collapse.svg` plots normalized contraction penalty against `K1-K2` for all admissible ratio pairs at fixed `epsilon=0.95`, separately for `kappa_bar in {2,10,100}`.

At fixed `kappa_bar` and `epsilon`, `K2` and the empirical step size are invariant. Therefore all admissible `(tau_L,tau_mu)` pairs with the same mismatch coordinate must produce the same inherited cubic and the same selected contraction factor. The figure visually tests this structural collapse.

This is the key Phase 19 visual: a two-dimensional heterogeneity surface becomes a one-dimensional rate curve once the correct coordinate is used.

## Reproducibility

Run

```bash
python scripts/build_phase19_figures.py
```

for the publication-resolution default (`101 x 101` ratio grid per conditioning stratum). The script writes:

```text
paper_assets/phase19_full_regularity/
  figure6_mismatch_geometry.svg
  figure7_full_regularity_penalty.svg
  figure8_rate_collapse.svg
  phase19_rate_collapse_data.csv
  phase19_figure_summary.json
```

CI uses a smaller `31 x 31` smoke build and uploads the resulting artifact.

## Claim guardrail

The figures visualize and stress-test structural consequences of the inherited two-agent Empirical Law 4.3. They must not be described as an independent proof of the empirical law or as a result for arbitrary numbers of agents.
