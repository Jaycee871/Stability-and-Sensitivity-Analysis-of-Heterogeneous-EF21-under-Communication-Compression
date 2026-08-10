# Phase 22 — Reviewer Pre-Mortem 2.0 and OSF Release-Candidate Gate

## Purpose

Phase 22 is the final pre-archive adversarial layer before the project is copied into an external Open Science Framework record. It has two goals:

1. attack the current manuscript as a skeptical reviewer would; and
2. define a reproducible local release candidate without pretending that an OSF registration or DOI already exists.

## Reviewer pre-mortem 2.0

The updated reviewer pre-mortem explicitly challenges the strongest current claims and possible misunderstandings, including:

- whether the work is only a reproduction;
- whether `K1-K2 = Var_w(q_i)` is merely elementary algebra;
- whether the fixed-average `(tau_L-tau_mu)^2` factorization is meaningful beyond a change of variables;
- why Empirical Law 4.3 itself is not proved;
- why the analysis remains restricted to `n=2`;
- how invalid `mu_i>L_i` cells are handled;
- why the equal-smoothness baseline is retained after the full-regularity extension;
- whether Figure 8 is merely a tautological replot;
- the distinction between numerical baseline monotonicity and analytic `d rho_star/dK1>0` sensitivity;
- whether the Wolfram certificate is independently reproducible;
- whether the literature audit establishes only scoped reference closure rather than universal novelty;
- how existing smoothness-only EF21 heterogeneity work is positioned;
- the lack of a large stochastic ML benchmark;
- reproducibility under multi-model AI assistance;
- editorial independence if the Special Issue Guest Editor is involved; and
- whether the OSF archive is genuinely frozen and permanent.

Every prepared response is tied back to Claim Registry v2 and its evidence-level guardrails.

## Scoped contribution statement

The former short novelty statement is replaced with a contribution-and-guardrail statement. It explicitly separates:

- inherited Empirical Law 4.3 objects;
- N1a as a non-novel algebraic reinterpretation;
- N1b–N4 as scoped project-derived analyses of the inherited cubic; and
- named-chain literature closure from universal bibliographic novelty.

Absolute precedence wording remains prohibited.

## OSF release-candidate builder

`scripts/build_osf_release_candidate.py` creates a deterministic local bundle containing the version-controlled scientific record:

```text
README.md
requirements.txt
src/
scripts/
tests/
results/
wolfram/
claims/
literature/
docs/
manuscript/
submission/
osf/osf_metadata_template.json
.github/workflows/ci.yml
```

When generated paper assets and the MDPI free-format package are supplied to the builder, they are copied under `generated/` and checked for required full-regularity figures and manuscript output.

The builder writes:

```text
ARCHIVE_README.md
OSF_ARCHIVE_MANIFEST.json
```

The manifest records:

- source Git commit;
- scientific-gate state;
- whether publication assets and the submission package were included;
- every bundled file path;
- file size;
- SHA-256 digest;
- total file count and byte count; and
- unresolved external OSF registration state.

A ZIP archive and compact `build_report.json` are emitted alongside the bundle.

## Scientific gate

Before the local release candidate is produced, the builder requires:

- Claim Registry version 2 with 18 claims;
- Phase 17 status `NAMED_REFERENCE_CHAIN_CLOSED`;
- `universal_novelty_certified=false`;
- the Phase 13 guardrail that explicitly states the certificate does not prove Empirical Law 4.3 itself;
- the Phase 20 manuscript state; and
- manuscript integration of Figures 6–8.

Failure of any of these checks blocks archive creation.

## OSF state semantics

The local candidate uses the state:

```text
READY_FOR_OSF_DRAFT_UPLOAD
```

This means only that the repository-side release gate passed. It does **not** mean:

- an OSF project has been created;
- the bundle has been uploaded;
- the record is public;
- the project is registered;
- a DOI has been minted; or
- the archive is permanently frozen.

Those claims become valid only after an external OSF record exists and its identifier/state are independently verified.

## Metadata placeholders

`osf/osf_metadata_template.json` intentionally leaves the following unresolved:

- final human contributor list;
- archive license;
- OSF identifier;
- DOI;
- registration state; and
- public/private state.

This prevents the local repository from fabricating metadata that has not yet been decided by the human authors.

## CI artifacts

Phase 22 CI builds and uploads two new artifacts:

```text
phase22-osf-release-candidate
phase22-reviewer-premortem
```

The reviewer artifact contains the updated pre-mortem, scoped contribution statement, terminology guardrails, Claim Registry v2 evidence matrix, and the OSF build report.

## Final guardrail

A successful Phase 22 CI run means the project has a reproducible **release candidate** suitable for human-controlled OSF upload. It is not evidence that an external archive already exists.
