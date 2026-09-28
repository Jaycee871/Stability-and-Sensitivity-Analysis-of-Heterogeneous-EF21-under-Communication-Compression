# Sensitivity of Two-Agent EF21 to Heterogeneous Regularity under Compression

> **Submitted manuscript title:** **Sensitivity of Two-Agent EF21 to Heterogeneous Regularity under Compression**  
> **GitHub repository name:** `Stability-and-Sensitivity-Analysis-of-Heterogeneous-EF21-under-Communication-Compression`

The repository name reflects an earlier working title of the project and is intentionally retained for continuity of the public repository history. The **submitted paper title is different from the repository name** and should be cited as **“Sensitivity of Two-Agent EF21 to Heterogeneous Regularity under Compression.”**

This repository contains the analysis code, numerical summaries, symbolic verification materials, and reproducibility scripts supporting the submitted manuscript **“Sensitivity of Two-Agent EF21 to Heterogeneous Regularity under Compression.”**

The study analyzes the two-agent cubic relation reported as Empirical Law 4.3 in Berg Thomsen, Taylor, and Dieuleveut, *A Tight Theory of Error Feedback Algorithms in Distributed Optimization*. In the manuscript, this reproduced relation is called the **Heterogeneity-Aware Convergence Law (HAC Law)**.

> **Scope guardrail:** the cubic relation and its empirical step size are inherited from the source paper. This repository reproduces and analyzes their consequences. It does not claim a new general convergence theorem for EF21.

## Submission status

- **Status:** Submitted
- **Journal:** *Mathematics* (MDPI)
- **Submission date:** 28 September 2026
- **Submitted title:** **Sensitivity of Two-Agent EF21 to Heterogeneous Regularity under Compression**
- **Authors:** Pack Kwan Low and Fu-Hsing Wang

The submitted PDF is stamped **“Version September 28, 2026 submitted to Mathematics.”** This repository now treats that submission as the manuscript version of record. Acceptance, publication details, and DOI are not yet recorded here.

## Submitted manuscript

The submitted LaTeX source of record is:

- [`manuscript/manuscript.tex`](manuscript/manuscript.tex)
- [`submission/manuscript_submitted_2026-09-28.tex`](submission/manuscript_submitted_2026-09-28.tex) — frozen submission snapshot

The older [`manuscript/draft.md`](manuscript/draft.md) and phase-numbered documents are retained as development records. For the 28 September 2026 submission, the frozen snapshot above is the archival source of record; `manuscript/manuscript.tex` is the maintained working copy.

## Study design

### Independent numerical reproduction

The source verification grid contains 20 local regularity configurations per worker, formed from four smoothness values and five condition numbers. Accounting for worker-exchange symmetry gives 210 unordered worker pairs. Evaluating each pair at 50 compression levels produces:

```text
210 x 50 = 10,500 configurations
```

The reproduction checks the cubic residual, agreement with the hash-pinned source implementation, agreement with the homogeneous theoretical limit, and rejection of a deliberately modified polynomial used as a negative control.

The maximum observed polynomial residual is `1.742e-15`. The maximum stored-precision difference from the source helper is zero, and the homogeneous-limit difference is at most `8.389e-13`.

### Equal smoothness analysis

The first controlled study sets `L1=L2=1`, fixes the arithmetic mean of `mu1` and `mu2`, and varies:

```text
tau = mu2 / mu1
epsilon in [0.01, 0.95]
kappa_bar in {2, 10, 100}
```

The dense audit contains:

```text
381 tau values x 189 epsilon values x 3 strata = 216,027 configurations
```

It evaluates the predicted contraction factor, absolute and normalized heterogeneity penalties, contraction-margin retention, 99% retention boundaries, grid refinement, and 20,000 additional off-grid parameter pairs.

### Full regularity analysis

The second controlled study allows smoothness and strong convexity to vary independently while holding both arithmetic means fixed:

```text
L_bar  = (L1 + L2) / 2
mu_bar = (mu1 + mu2) / 2
tau_L  = L2 / L1
tau_mu = mu2 / mu1
```

The audit requests `273,885` parameter cells, of which `258,400` satisfy `0 < mu_i <= L_i`.

Define

```text
q_i = (L_i - mu_i) / (L_i + mu_i)
w_i = (L_i + mu_i) / [(L1 + mu1) + (L2 + mu2)]
```

Then the mismatch coordinate is

```text
Psi = K1 - K2 = sum_i w_i (q_i - sum_j w_j q_j)^2 >= 0.
```

Under the fixed average parameterization, the empirical step size and `K2` are invariant. The remaining regularity dependence is carried by `Psi`, whose exact factorization contains `(tau_L-tau_mu)^2`. Therefore `Psi=0` exactly on the proportional path `tau_L=tau_mu`.

### Root sensitivity and the exact-transmission endpoint

For `0<epsilon<1` and the stated admissible domain, the symbolic certificate establishes three distinct roots in `(0,1)` and a simple selected largest root. At fixed `K2`, the selected root increases with `K1`, and hence with `Psi`.

At `epsilon=0`, the cubic reduces to

```text
Q(rho) = rho^2 (rho-K2).
```

When `K2>0`, the selected largest root is `rho_star=K2` and `d rho_star/dK1=0`. When `K2=0`, zero has multiplicity three. The strict positive-sensitivity statement is therefore restricted to `0<epsilon<1`.

## Main manuscript findings

1. In the equal smoothness setting, stronger convexity heterogeneity reduces the available contraction margin.
2. Heavier compression amplifies the relative heterogeneity penalty.
3. Under the fixed average parameterization, the empirical step size and `K2` remain invariant.
4. The remaining regularity dependence reduces to the nonnegative mismatch measure `Psi=K1-K2`.
5. Proportional variation of smoothness and strong convexity produces zero mismatch even when the workers remain heterogeneous.
6. Conditional on the reproduced HAC Law, the selected contraction root increases with mismatch.

## Repository map

```text
manuscript/manuscript.tex       current author-reviewed manuscript
manuscript/figure_captions_current.md  captions used in the current manuscript
src/ef21_stability/             core numerical implementation
scripts/                        grid, robustness, figure, and audit scripts
results/                        numerical and symbolic summary files
wolfram/                        independent symbolic verification
claims/                         scoped claim registry
docs/                           development and audit records
submission/                     submitted-source snapshot, status, and support materials
tests/                          unit and regression tests
```

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

# Optional independent symbolic verification
wolframscript -file wolfram/phase13_full_structure_proof.wl
```

## Provenance

The independent reproduction from which this sensitivity study developed is available at:

- https://github.com/Jaycee871/-26468-A-Tight-Theory-of-Error-Feedback-Algorithms-in-Distributed-Optimization

Historical phase documents remain available for auditability, but their project-stage terminology should not be substituted for the terminology of the current manuscript.
