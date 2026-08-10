# Phase 22 — Reviewer Pre-Mortem 2.0

This document anticipates the strongest technical, methodological, and editorial objections to the current full-regularity manuscript. It is not a rebuttal letter. It is an adversarial quality-control layer: every prepared response must remain within the evidence level registered in `claims/claim_registry.json`.

## 1. “Is this still only a reproduction paper?”

**Risk:** The cubic, `K1`, `K2`, and the empirical optimal step size all originate in Thomsen, Taylor, and Dieuleveut.

**Prepared response:** Yes, the inherited empirical law is the starting object, and the manuscript says so explicitly. The extension is the controlled characterization around that object: the equal-smoothness compression–heterogeneity baseline, the full `(tau_L,tau_mu)` fixed-average parameterization, the exact mismatch factorization, aligned-path invariance, generic inherited-cubic root localization and sensitivity, and reproducible publication figures. The manuscript never relabels the source cubic as its own theorem.

**Evidence:** C01–C18 in `claims/claim_registry.json`; especially C09 and C11–C17.

**Firewall:** The words **inherited**, **Empirical Law 4.3**, and the conditional scope must remain visible wherever the cubic is interpreted.

---

## 2. “Is `K1-K2 = Var_w(q_i)` merely elementary algebra?”

**Risk:** A reviewer may correctly observe that the weighted-variance identity follows immediately from the source definitions of `K1` and `K2`.

**Prepared response:** Correct. The manuscript explicitly classifies this as an **inherited algebraic reinterpretation**, not a theorem-level contribution. Its purpose is explanatory: it identifies `K1` as a weighted second moment and `K2` as the squared weighted mean of the local condition-shape coordinate. The scoped structural contribution begins with the fixed-average factorization in `(kappa_bar,tau_L,tau_mu)`, not with the variance identity itself.

**Evidence:** C12; `literature/phase17_primary_source_closure.json` → `claims.N1a.status`.

**Firewall:** Never write that the project “introduces a new variance measure” or that N1a itself is novel.

---

## 3. “Is the `(tau_L-tau_mu)^2` factorization mathematically deep enough?”

**Risk:** The exact factorization may be viewed as a change of variables rather than a stand-alone theoretical breakthrough.

**Prepared response:** The paper does not sell the factorization in isolation. Its value is the structural chain it unlocks under a controlled experimental design: fixed arithmetic means make the empirical step size and `K2` invariant; the remaining coefficient dependence is a nonnegative mismatch gap; the gap vanishes exactly on proportional regularity scaling; and the generic cubic sensitivity converts that algebraic gap into an ordered rate consequence. The contribution is the combined controlled characterization, not the complexity of one algebraic manipulation.

**Evidence:** C11, C13, C14, C16, C17.

**Firewall:** Use “derive,” “factor,” and “show,” not claims of a new general optimization theorem.

---

## 4. “Why analyze an empirical law instead of proving Empirical Law 4.3 itself?”

**Risk:** A mathematically oriented reviewer may demand proof of the source empirical law.

**Prepared response:** The study deliberately solves a different problem: conditional structural and sensitivity analysis of the inherited cubic. Phase 13 proves exact algebraic and root-structure consequences **if that inherited cubic is taken as the object being characterized**. A proof that the cubic equals the true worst-case EF21 convergence factor for every heterogeneous problem would require a separate PEP/interpolation or Lyapunov argument and is outside the scope claimed here.

**Evidence:** C09, C15–C17; `results/phase13_symbolic_certificate.json` guardrail.

**Firewall:** Never say “we prove Empirical Law 4.3” or “we establish the heterogeneous EF21 convergence theorem.”

---

## 5. “Why only two agents?”

**Risk:** Limited external validity.

**Prepared response:** The two-agent restriction is inherited from the explicit empirical cubic being studied. The manuscript chooses a well-defined `n=2` mathematical object rather than extrapolating unsupported formulas to arbitrary worker count. Related PEP symmetry work motivates why low-agent cases can reveal structure, but it does not authorize generalization of the present cubic.

**Evidence:** C09, C14–C17; Methods §2.2 and §3.5.

**Limitation:** No arbitrary-`n` claim.

---

## 6. “Does the full-regularity grid include impossible local objectives?”

**Risk:** Independent variation of `tau_L` and `tau_mu` can create `mu_i>L_i`.

**Prepared response:** Such cells are explicitly excluded. The full audit requests `273,885` cells and retains `258,400` that satisfy `0<mu_i<=L_i`; `15,485` invalid regularity cells are masked rather than coerced. The figures preserve the mask.

**Evidence:** C10; `results/phase12_summary.json`.

**Firewall:** Never interpolate a scientific conclusion through the masked region as though it were admissible.

---

## 7. “Why retain the old `L1=L2` baseline after introducing full regularity?”

**Risk:** The manuscript may look like two unrelated studies.

**Prepared response:** The equal-smoothness stage is the controlled baseline that first separates strong-convexity heterogeneity from average conditioning and quantifies the compression interaction. The full-regularity stage then asks what changes when smoothness heterogeneity is released. The second stage explains the first: the equal-smoothness path is one particular mismatch trajectory inside the larger `(tau_L,tau_mu)` surface.

**Evidence:** C01–C06 and C10–C17; Results §4.1–§4.9.

**Action:** Preserve the narrative transition from “heterogeneity magnitude” to “regularity mismatch.”

---

## 8. “Is Figure 8 just a tautological replot?”

**Risk:** Because `K2` is fixed and `K1-K2` determines `K1`, plotting rate against the mismatch coordinate may seem predetermined.

**Prepared response:** Figure 8 is not presented as independent proof. It is a publication visualization and regression check of the structural reduction established algebraically. Its scientific role is communicative: thousands of admissible two-dimensional parameter pairs collapse onto the one-dimensional coordinate predicted by the exact coefficient analysis. The proof burden remains on C11–C17, not on the scatter plot.

**Evidence:** C11–C17; `docs/phase19_full_regularity_figures.md`; `tests/test_phase19_figures.py`.

**Firewall:** Do not describe the visual collapse as an independent theorem or empirical discovery separate from the coefficient reduction.

---

## 9. “Have you proved monotonicity, or only observed it?”

**Risk:** The manuscript now contains two different monotonicity evidence levels.

**Prepared response:** They must be distinguished. The original equal-smoothness monotonic patterns are computational observations supported by dense and off-grid tests. The later statement `d rho_star/dK1>0` is an analytic-symbolic result about the inherited cubic on the stated generic shape-coordinate domain. It does **not** prove global monotonicity of EF21 with respect to every raw heterogeneity parameter.

**Evidence:** C06 versus C16–C17.

**Firewall:** Keep “across the audited grid” for baseline raw-parameter trends; reserve the strict derivative statement for the inherited cubic coordinate `K1`.

---

## 10. “Why trust the Wolfram result?”

**Risk:** Symbolic computer algebra can hide assumptions or model-generated mistakes.

**Prepared response:** The Wolfram layer is an independent computation engine, not a language-model assertion. The repository preserves the exact `.wl` proof script, machine-readable certificate, Python regression tests, and numerical cross-checks. The proof statement is additionally constrained by explicit domain assumptions (`0<s<1`, `0<K2<=K1<1`) and an evidence registry.

**Evidence:** C15–C17; `wolfram/phase13_full_structure_proof.wl`; `results/phase13_symbolic_certificate.json`; `tests/test_phase13_symbolic_certificate.py`.

**Firewall:** Do not claim that “AI proved” the result. The evidence is the reproducible symbolic computation and the recorded mathematical argument.

---

## 11. “Did the literature audit merely fail to find a counterexample?”

**Risk:** Negative search results can be overstated as universal novelty.

**Prepared response:** The project deliberately does not make a universal novelty claim. Undermind supplied an adversarial shortlist; Claude supplied a second targeted search and exposed remaining coverage gaps; Phase 17 then closed the named source-paper citation chain by primary-source inspection. The recorded result is `NAMED_REFERENCE_CHAIN_CLOSED` with `universal_novelty_certified=false`. This supports scoped contribution wording, not “first” or “no prior work.”

**Evidence:** C18; `literature/phase17_primary_source_closure.json`; Phase 14–17 audit records.

**Firewall:** Absolute bibliographic precedence remains blocked.

---

## 12. “What about prior smoothness-heterogeneity and variance-style EF21 analyses?”

**Risk:** Error Feedback Reloaded already analyzes heterogeneous smoothness and a variance-like smoothness dispersion.

**Prepared response:** It must be cited and positioned. The manuscript does not claim that heterogeneity or variance-style reasoning is absent from EF21 theory. The narrower object here jointly involves local `L_i` and `mu_i`, fixed arithmetic means, the inherited `K1/K2` cubic coordinates, proportional-alignment invariance, and conditional root sensitivity.

**Evidence:** Related Work §2.3; Phase 15–17 literature audit.

**Firewall:** Never write “first variance-based EF21 heterogeneity characterization.”

---

## 13. “Where is the practical value without a large ML benchmark?”

**Risk:** Applied reviewers may request end-to-end training experiments.

**Prepared response:** The paper is a controlled mathematical/computational characterization, not an empirical benchmark study. Its practical outputs are sensitivity maps, contraction-margin retention, admissibility masks, and a structural distinction between aligned heterogeneity and mismatch. A stochastic large-scale benchmark would add optimizer/data/architecture effects that do not independently validate the inherited worst-case cubic.

**Limitation:** Do not infer large-scale stochastic ML behavior from this study.

---

## 14. “How reproducible is a study built with multiple AI systems?”

**Risk:** A reviewer may worry that results depend on opaque model output.

**Prepared response:** AI systems were used for research assistance, search, code drafting/review, and manuscript support, but scientific evidence is version-controlled and independently checkable. Numerical results are regenerated by Python and CI; symbolic results are reproduced by Wolfram Language; literature-search outputs are treated as candidate evidence until manually adjudicated against primary sources; the 18-claim registry fails if manuscript anchors or evidence paths drift.

**Evidence:** Phase 21 claim registry; manuscript §3.9; `submission` AI disclosure; GitHub Actions workflow.

**Firewall:** Human authors remain responsible for source verification, code/result review, and the final claims.

---

## 15. “Does the Guest Editor relationship create an editorial conflict?”

**Risk:** The academic-advisor relationship can create an actual or perceived editorial conflict.

**Prepared response:** The relationship is disclosed and independent editorial handling is requested. The Guest Editor should not select reviewers or participate in the editorial decision for the manuscript. If the Guest Editor becomes a co-author, the conflict wording must be revised accordingly while independent handling remains essential.

**Evidence:** `submission/editorial_independence_note.md` and `submission/mdpi_policy_snapshot.md`.

---

## 16. “Is the OSF record actually frozen and reproducible?”

**Risk:** A repository URL alone is not a permanent research snapshot.

**Prepared response:** Phase 22 creates a deterministic OSF release-candidate bundle with a SHA-256 inventory before any OSF registration/DOI is claimed. The bundle contains source code, tests, committed evidence, Wolfram scripts, literature-audit records, manuscript sources, and submission metadata. The project will not fill the manuscript's permanent archive placeholder until the bundle is uploaded and the resulting OSF identifier is verified.

**Evidence:** `scripts/build_osf_release_candidate.py`; Phase 22 CI artifact; generated `OSF_ARCHIVE_MANIFEST.json`.

**Firewall:** `READY_FOR_OSF_DRAFT_UPLOAD` is not equivalent to “OSF archived,” “registered,” or “DOI assigned.”

---

## Pre-submission decision rule

A revision is not accepted merely because it sounds stronger. If wording exceeds the evidence level in Claim Registry v2, either new evidence must be added and audited or the wording must remain scoped. Likewise, an archive is not called permanent until an external OSF identifier exists and has been independently checked.
