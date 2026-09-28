# Current manuscript terminology guardrails

These terms follow the author-reviewed manuscript.

## Preferred terms

- **Heterogeneity-Aware Convergence Law (HAC Law):** the reproduced two-agent cubic relation reported as Empirical Law 4.3 in the source paper.
- **independent numerical reproduction:** the 10,500-configuration replay and its numerical consistency checks.
- **equal smoothness setting / equal smoothness analysis:** the controlled setting with `L1=L2=1` and fixed average strong convexity.
- **full regularity setting / full regularity analysis:** the setting in which local smoothness and local strong convexity vary independently.
- **fixed average parameterization:** the full regularity construction holding the arithmetic means of smoothness and strong convexity fixed.
- **homogeneous theoretical limit:** the comparison with the proved homogeneous EF21 contraction rate.
- **regularity mismatch:** `Psi=K1-K2`, the weighted variance of the local regularity ratios.
- **alignment invariance:** insensitivity of the reproduced cubic to proportional regularity scaling along `tau_L=tau_mu`.

Do not use hyphenated labels such as `equal-smoothness`, `full-regularity`, `fixed-average`, or `homogeneous-limit` as manuscript terminology.

## Evidence language

Use **reproduced**, **numerical consistency**, **conditional on the reproduced empirical relation**, and **predicted contraction factor**. Do not describe the reproduction as an independent proof of the heterogeneous EF21 convergence law.

The polynomial residual, source-helper agreement, homogeneous theoretical limit, and negative controls support numerical consistency of the implementation. They do not convert Empirical Law 4.3 into a theorem.

## Exact transmission

At `epsilon=0`, `Q(rho)=rho^2(rho-K2)`. If `K2>0`, the selected largest root is `K2` and its derivative with respect to `K1` is zero. If `K2=0`, zero is a triple root. Therefore the later strict mismatch-sensitivity statement applies only to `0<epsilon<1`.

## Historical records

Phase-numbered files document the development process and may contain older wording. The authoritative manuscript terminology is the wording in `manuscript/manuscript.tex`.
