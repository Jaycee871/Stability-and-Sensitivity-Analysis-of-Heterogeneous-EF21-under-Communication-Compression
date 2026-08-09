# Phase 10 — Reviewer Pre-Mortem

This document anticipates likely technical and editorial objections before submission. It is not a rebuttal letter; it is a quality-control checklist for strengthening the manuscript without broadening the research scope.

## 1. “Is this only a reproduction paper?”

**Risk:** The source cubic law is inherited from Thomsen, Taylor, and Dieuleveut, so a reviewer may question novelty.

**Prepared response:** The reproduction is the validated starting point, not the manuscript contribution. The extension introduces a controlled fixed-average heterogeneity path, maps the joint `(tau, epsilon, kappa_bar)` response over 216,027 configurations, defines contraction-margin retention, constructs operating boundaries, stress-tests those boundaries off-grid and under resolution refinement, and adds an independent fixed-stratum symbolic root-structure result. None of those outputs is the original six-claim reproduction itself.

**Evidence:** C01–C08 in `claims/claim_registry.json`; `docs/phase2_findings.md` through `docs/phase5_manuscript_plan.md`.

**Manuscript firewall:** Always describe the cubic and empirical optimal step size as **inherited**. Describe the controlled parameterization, retention analysis, robustness audit, and symbolic fixed-stratum result as the extension.

---

## 2. “Why analyze an empirical law instead of proving it?”

**Risk:** A mathematically oriented reviewer may ask for a proof of Empirical Law 4.3.

**Prepared response:** The source paper itself labels the general heterogeneous two-agent result empirical. The present study deliberately addresses a different question: conditional mathematical/computational characterization of that inherited law. This is analogous to sensitivity analysis of a validated model: the conclusions are explicitly conditional on the inherited cubic characterization. A full proof would be a different and substantially larger project.

**Evidence:** C09; source-paper citation `thomsen2026tight`.

**Manuscript firewall:** Never use “prove Empirical Law 4.3,” “establish the heterogeneous EF21 theorem,” or equivalent language.

---

## 3. “Why only two agents?”

**Risk:** Limited external validity.

**Prepared response:** The two-agent restriction is structural rather than arbitrary: Empirical Law 4.3 supplies the explicit cubic only for `n=2`. The study intentionally avoids replacing a well-defined inherited object with an unsupported extrapolation to larger `n`. The two-agent setting is used as a controlled laboratory for separating compression, average conditioning, and local-curvature imbalance.

**Evidence:** Methods Section 3.1; C09.

**Limitation to retain:** No claims about arbitrary worker count.

---

## 4. “Why set `L1=L2=1`?”

**Risk:** Reviewer may view equal smoothness scales as overly restrictive.

**Prepared response:** Fixing `L1=L2` and normalizing the common scale isolates heterogeneity in strong convexity while avoiding simultaneous changes in scale and average conditioning. Scale invariance was independently checked, so `L=1` is a normalization rather than a hidden performance assumption. The purpose is controlled attribution, not maximal parameter coverage.

**Evidence:** Phase 1 scale-invariance tests; Phase 4 Wolfram scale-invariance result.

**Limitation to retain:** The conclusions do not cover independent heterogeneity in both `L_i` and `mu_i`.

---

## 5. “Is ‘stability analysis’ the correct term?”

**Risk:** In control/dynamical-systems language, “stability” can imply a Lyapunov or asymptotic-stability theorem.

**Prepared response:** Here “stability” refers to the robustness and parameter sensitivity of the inherited contraction-rate characterization: root admissibility, contraction-margin loss, operating-boundary stability under grid refinement, and absence of root-collision transitions on the tested fixed-conditioning domains. The manuscript does **not** claim a new Lyapunov-stability theorem for EF21.

**Action:** Keep the terminology definition in `manuscript/terminology_guardrails.md` available for Introduction/Methods wording during final template transfer.

---

## 6. “Why choose 99% contraction-margin retention?”

**Risk:** The threshold can appear arbitrary.

**Prepared response:** Ninety-nine percent is an interpretable high-retention operating criterion, not a theoretically privileged constant. The repository also evaluates 98% and 95% targets, showing how the boundary changes as the decision tolerance is relaxed. The main text uses 99% because it exposes the interaction clearly while retaining a simple operational interpretation.

**Evidence:** `results/phase3_summary.json`, `retention_targets=[0.99,0.98,0.95]`.

**Manuscript firewall:** Call it a **chosen operating criterion**, never a universal stability threshold.

---

## 7. “Why does worse conditioning appear more robust to heterogeneity?”

**Risk:** Misinterpretation of the small normalized penalty at `kappa_bar=100`.

**Prepared response:** It is not more robust in an absolute convergence sense. Every audited cell in that stratum already has `rho_star>=0.95`, and about 63.5% have `rho_star>=0.99`. The baseline has little contraction margin left to lose, so the incremental relative heterogeneity effect appears small.

**Evidence:** C04.

**Manuscript firewall:** Never equate smaller heterogeneity penalty with faster convergence.

---

## 8. “Have you proved monotonicity in heterogeneity or compression?”

**Risk:** Dense plots can tempt stronger wording than the evidence supports.

**Prepared response:** No. The manuscript reports monotone behavior on the audited regular grid and deterministic off-grid paired stress tests under a stated numerical tolerance. The `kappa_bar=100` off-grid compression audit even preserves a small positive ordering residual of about `3.7e-10`, below the `1e-9` interpretation tolerance, rather than concealing it.

**Evidence:** C06; `results/phase4_summary.json`.

**Manuscript firewall:** Use “across the audited grid,” “within numerical tolerance,” and “off-grid checks support,” not “globally monotone.”

---

## 9. “What does the positive discriminant actually add?”

**Risk:** Reviewer may see the Wolfram result as decorative algebra.

**Prepared response:** It excludes root-collision transitions as the mechanism behind the observed sensitivity patterns on each tested fixed-conditioning open domain. Because the discriminant is strictly positive, the cubic stays in a three-distinct-real-root regime; the numerical sensitivity therefore reflects continuous movement of the relevant root rather than a change in root multiplicity.

**Evidence:** C07–C08.

**Manuscript firewall:** The discriminant result characterizes root structure; it does not validate the empirical convergence law itself.

---

## 10. “Where is the practical value if there is no large ML benchmark?”

**Risk:** Applied reviewer may request end-to-end training experiments.

**Prepared response:** The study's practical output is a parameter-selection map conditional on an inherited tight-rate model, not a benchmark paper. The retention boundary translates the cubic rate into an interpretable loss-of-margin criterion. Adding a large stochastic training benchmark would introduce optimizer, data, architecture, and noise effects that are outside the controlled question and would not independently validate the worst-case cubic law.

**Limitation to retain:** Do not infer large-scale stochastic ML behavior from the present analysis.

---

## 11. “How reproducible are the results?”

**Prepared response:** All headline numerical statements are regenerated by version-controlled Python, checked in CI, mapped through a nine-claim evidence registry, and packaged with full-resolution figures/tables. The symbolic statements are independently evaluated with Wolfram Language. Hugging Face authentication is available for artifact publication, and OSF archival is planned before final submission.

**Evidence:** Phase 8 and Phase 9 CI artifacts; `claims/claim_registry.json`.

---

## 12. “Does the Guest Editor relationship create an editorial conflict?”

**Prepared response:** The academic-advisor relationship will be disclosed and independent editorial handling requested. The Guest Editor should not participate in the editorial decision for this manuscript.

**Evidence:** `submission/editorial_independence_note.md` and `submission/mdpi_policy_snapshot.md`.

---

## Pre-submission decision rule

A revision should not be accepted merely because it sounds stronger. If it expands a claim beyond the evidence level recorded in `claims/claim_registry.json`, either new evidence must be added and audited or the wording must remain scoped.
