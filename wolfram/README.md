# Wolfram symbolic bridge

This directory adds an optional Wolfram Language layer to the Python-first EF21 study. The Python implementation remains the reproducibility baseline; Wolfram is used for independent symbolic simplification, discriminant analysis, root cross-checking, and possible discovery of semi-algebraic parameter boundaries.

## Files

- `ef21_symbolic.wl` — controlled two-agent EF21 formulas, cubic polynomial, numerical root, retention metric, and symbolic checks.
- `reference_cases.json` — engine-neutral test inputs shared by Wolfram and Python.
- `export_reference.wl` — evaluates the shared cases in Wolfram and exports `outputs/wolfram_reference.json`.
- `cloud_api.wl` — restricted Cloud API template. It exposes only four fixed actions and never evaluates arbitrary user expressions.

## Option A: run locally with Wolfram Engine / Mathematica

From the repository root:

```bash
wolframscript -file wolfram/export_reference.wl
python scripts/compare_wolfram_reference.py wolfram/outputs/wolfram_reference.json
```

A successful comparison means the Wolfram and Python engines agree on the pinned cases for:

- cubic coefficients,
- largest admissible real root,
- homogeneous Theorem 3.1 rate,
- contraction-margin retention,
- cubic discriminant.

The generated JSON should be committed when it is used as research evidence so the Wolfram version and numerical results remain auditable.

## Option B: Wolfram Cloud notebook

1. Open a Wolfram Cloud notebook.
2. Upload or paste `ef21_symbolic.wl` and evaluate it.
3. Evaluate `SymbolicReport[]` to inspect scale invariance, the homogeneous step-size limit, homogeneous `K1/K2`, and the cubic discriminant.
4. For API use, upload/evaluate `cloud_api.wl` after `ef21_symbolic.wl`.

`cloud_api.wl` defaults to:

```wolfram
$EF21APIPermissions = "Private";
```

If an external read-only client must query the endpoint, intentionally change it to:

```wolfram
$EF21APIPermissions = "Public";
```

and redeploy. The endpoint still accepts only the fixed actions `coefficients`, `roots`, `retention`, and `discriminant`; there is no arbitrary-expression evaluation path.

## API contract

The API parameters are:

```text
action   coefficients | roots | retention | discriminant
tau      0 < tau <= 1
epsilon  0 < epsilon < 1
kappa    kappa_bar >= 1
```

Example query semantics:

```text
action=retention, tau=0.18, epsilon=0.95, kappa=10
```

The response is JSON and includes the supplied parameters plus the requested result.

## Research role

Wolfram output is treated as an independent symbolic/numerical cross-check, not as a replacement for the Python pipeline and not as proof by itself. Any symbolic statement promoted into the manuscript should be exported, cross-checked where possible, and stated with its exact parameter assumptions.
