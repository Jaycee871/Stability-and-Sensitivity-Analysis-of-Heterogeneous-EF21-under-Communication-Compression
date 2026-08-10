# Phase 20 — Manuscript and Submission Integration of Full-Regularity Figures

## Purpose

Phase 19 established the three full-regularity publication figures as reproducible CI artifacts. Phase 20 moves them into the actual paper pipeline so that the visual evidence, manuscript discussion, and MDPI free-format package cannot drift apart.

## Integrated figures

### Figure 6 — mismatch geometry

Inserted after Results §4.7. The figure visualizes the exact `K1-K2` surface and the zero-mismatch diagonal `tau_L=tau_mu`.

### Figure 7 — aligned zero-penalty valley

Inserted after Results §4.8. The figure places the same aligned diagonal in rate space and shows that proportional regularity heterogeneity leaves the inherited cubic at the homogeneous controlled prediction.

### Figure 8 — one-coordinate rate collapse

Inserted after Results §4.9. The figure plots normalized contraction penalty against `K1-K2` and visually demonstrates that, at fixed conditioning and compression, the two-dimensional `(tau_L,tau_mu)` surface collapses onto the single inherited-cubic mismatch coordinate.

## Asset pipeline

`build_paper_assets.py` now runs the Phase 19 builder as part of the integrated asset build. Its manifest contains nine figures:

```text
figures/figure1_contraction_landscape.svg
figures/figure2_normalized_penalty.svg
figures/figure3_conditioning_interaction.svg
figures/figure4_retention_boundary.svg
figures/figure5_boundary_convergence.svg
figures/figureS1_symbolic_root_structure.svg
phase19_full_regularity/figure6_mismatch_geometry.svg
phase19_full_regularity/figure7_full_regularity_penalty.svg
phase19_full_regularity/figure8_rate_collapse.svg
```

The underlying Phase 19 rate-collapse CSV is copied with the paper assets.

The publication default retains a `101 x 101` full-regularity ratio grid. CI uses `31 x 31` for the integrated smoke build.

## Submission pipeline

`build_submission_package.py` now requires captions and manuscript markers for Figures 6–8. The generated MDPI free-format source replaces those markers with explicit insertion positions and full captions, while the integrated SVG files are copied into the submission package under:

```text
paper_assets/phase19_full_regularity/
```

A missing marker, caption, or asset therefore fails a regression test rather than silently producing an incomplete package.

## Claim guardrail

Figure integration does not change claim scope. Figures 6–8 visualize consequences of the inherited two-agent Empirical Law 4.3 under the controlled fixed-average parameterization. They do not prove Empirical Law 4.3 itself, do not generalize the result beyond `n=2`, and do not support absolute bibliographic novelty wording.
