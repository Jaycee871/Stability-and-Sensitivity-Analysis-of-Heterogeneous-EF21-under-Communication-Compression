# Phase 14 — Undermind Literature Novelty Audit Protocol

## Purpose

Phases 11–13 produced a controlled full-heterogeneity characterization of the inherited two-agent EF21 Empirical Law 4.3. Before promoting those findings into the manuscript, Phase 14 asks a literature question rather than a numerical one:

> Have the same structural objects or mathematically equivalent conclusions already appeared in distributed optimization, compressed/error-feedback optimization, performance-estimation analysis, or related heterogeneous strongly convex optimization literature?

This phase is designed as an **adversarial novelty audit**. Its purpose is to find the strongest prior art that could weaken or supersede our novelty claim, not to search only for papers that make the project look new.

Absence from one search system is not proof of novelty. Every candidate must be checked at the equation/theorem level before being labeled direct prior art or non-overlapping work.

---

## 1. Claims that must be challenged

### N1 — Weighted-variance mismatch coordinate

Under fixed arithmetic means, the inherited cubic coordinates satisfy

\[
K_2=\left(\frac{\bar\kappa-1}{\bar\kappa+1}\right)^2,
\]

and

\[
K_1-K_2
=\operatorname{Var}_{w}\!\left(
\frac{L_i-\mu_i}{L_i+\mu_i}
\right).
\]

For two agents this becomes

\[
K_1-K_2=
\frac{4\bar\kappa^2(\tau_L-\tau_\mu)^2}
{(\bar\kappa+1)^2
(\tau_L+\bar\kappa\tau_\mu+\bar\kappa+1)
(\bar\kappa\tau_L\tau_\mu+\tau_L\tau_\mu+\bar\kappa\tau_L+\tau_\mu)}.
\]

Challenge question: **Has prior work identified the same weighted variance, an algebraically equivalent quantity, or a directly equivalent local-condition-shape dispersion measure?**

### N2 — Aligned proportional heterogeneity invariance

When

\[
\tau_L=\tau_\mu,
\]

local smoothness and strong-convexity parameters scale proportionally. Then

\[
K_1=K_2,
\]

and the inherited cubic is exactly the homogeneous controlled cubic at the same average conditioning and compression.

Challenge question: **Has prior work shown that proportional heterogeneity in local smoothness and strong convexity becomes invisible, reducible to the homogeneous case, or otherwise leaves an equivalent convergence/spectral factor unchanged?**

### N3 — Monotonic penalty in the active mismatch coordinate

Phase 13 proves, conditional on the inherited empirical cubic, that

\[
\frac{d\rho^\star}{dK_1}>0
\]

on

\[
0<s<1,\qquad 0<K_2<1,\qquad K_2\le K_1<1.
\]

Because fixed average conditioning fixes `K2`, increasing the mismatch coordinate strictly worsens the inherited largest-root contraction factor.

Challenge question: **Has prior work proved an equivalent monotonic spectral-radius, contraction-factor, or rate degradation with a mismatch/variance coordinate involving local regularity?**

### N4 — Generic cubic root structure

On the same generic shape-coordinate domain, Phase 13 establishes for the inherited cubic:

- positive discriminant;
- three distinct real roots;
- all roots in `(0,1)`;
- largest root `rho_star > sqrt(epsilon)`.

Challenge question: **Has this generic root structure, or an equivalent cubic/spectral characterization, already been derived for EF21, error feedback, compressed distributed optimization, or related PEP formulations?**

---

## 2. Exact Undermind prompt

Paste the following prompt into Undermind without shortening the equations or replacing them with a broad request such as “find papers about EF21 heterogeneity.”

```text
I am conducting an adversarial novelty audit for a mathematical/computational extension of the two-agent heterogeneous EF21 result in “A Tight Theory of Error Feedback Algorithms in Distributed Optimization” (Thomsen, Taylor, Dieuleveut; Empirical Law 4.3).

Please search broadly across distributed optimization, communication compression, error feedback, EF21/EF-type methods, performance estimation problems (PEP), interpolation-based worst-case analysis, heterogeneous smooth strongly convex optimization, decentralized/federated optimization, spectral-radius analyses, and local condition-number heterogeneity.

The goal is NOT to find generally related papers. The goal is to determine whether any prior work contains a mathematical result equivalent or close enough to challenge novelty of the following four claims.

CLAIM N1 — weighted-variance mismatch coordinate.
For local smoothness L_i and strong convexity mu_i define
q_i=(L_i-mu_i)/(L_i+mu_i),
Sigma_i=L_i+mu_i,
w_i=Sigma_i/sum_j Sigma_j.
The inherited two-agent cubic coordinates satisfy
K1=sum_i w_i q_i^2,
K2=(sum_i w_i q_i)^2,
so
K1-K2=Var_w(q_i)>=0.
Under fixed arithmetic means L_bar and mu_bar, with kappa_bar=L_bar/mu_bar, tau_L=L2/L1, tau_mu=mu2/mu1,
K2=((kappa_bar-1)/(kappa_bar+1))^2
and
K1-K2 = 4*kappa_bar^2*(tau_L-tau_mu)^2 / [(kappa_bar+1)^2*(tau_L+kappa_bar*tau_mu+kappa_bar+1)*(kappa_bar*tau_L*tau_mu+tau_L*tau_mu+kappa_bar*tau_L+tau_mu)].

CLAIM N2 — aligned proportional heterogeneity invariance.
When tau_L=tau_mu, both agents’ L_i and mu_i scale proportionally, K1=K2, and the inherited Empirical Law 4.3 cubic exactly coincides with the homogeneous controlled cubic at the same average conditioning and compression. Thus proportional regularity heterogeneity is invisible to this inherited cubic; mismatch between smoothness and strong-convexity heterogeneity is the active structural deviation.

CLAIM N3 — monotonic mismatch penalty.
For s=sqrt(epsilon), 0<s<1, and cubic shape coordinates 0<K2<1, K2<=K1<1, the selected largest real root rho_star of the inherited cubic satisfies
 d rho_star / d K1 > 0.
At fixed average conditioning K2 is constant, so increasing K1-K2 strictly worsens the inherited predicted contraction factor.

CLAIM N4 — generic cubic root structure.
For the inherited cubic Q(rho) of Empirical Law 4.3, on 0<s<1 and 0<K2<1, K2<=K1<1, the discriminant is positive; Q has three distinct real roots; all roots lie in (0,1); and the largest root satisfies rho_star>s.

For EACH potentially relevant paper:
1. Give full citation, DOI/arXiv/OpenReview identifier, and stable URL if available.
2. Identify the exact theorem, proposition, lemma, equation, appendix, or page that is relevant.
3. Reproduce only the minimum mathematical notation needed to compare the result.
4. State whether the paper uses heterogeneous L_i and mu_i simultaneously, or only one type of heterogeneity.
5. State whether average/global conditioning is held fixed or changes with heterogeneity.
6. Determine whether its heterogeneity measure is algebraically equivalent to K1-K2 or Var_w((L_i-mu_i)/(L_i+mu_i)). Do not claim equivalence from verbal similarity; show the algebraic mapping or say it is unverified.
7. Determine whether it contains an aligned-proportional invariance result equivalent to tau_L=tau_mu.
8. Determine whether it proves monotonic degradation of a contraction factor/spectral radius/rate with an equivalent mismatch coordinate.
9. Determine whether it derives the same or equivalent cubic root structure.
10. Classify the candidate as:
   A = direct prior art / mathematically equivalent,
   B = materially overlapping but not equivalent,
   C = adjacent concept only,
   D = not relevant after inspection.
11. Explain in 2–5 sentences why the classification is justified.

Search older foundational literature as well as recent papers and preprints. Follow citation chains backward and forward from the EF21/error-feedback literature and from heterogeneous smooth strongly convex distributed optimization.

Be deliberately skeptical of novelty. Prefer a false alarm that we can inspect over missing a mathematically equivalent prior result.

At the end, provide:
A. the strongest direct-prior-art candidate for each of N1–N4;
B. a table comparing our four claims against the closest prior work;
C. a list of search terms and citation chains used;
D. a “novelty remains plausible / partially overlapped / likely not novel” judgment for each claim, with confidence level;
E. explicit unresolved equivalence checks that still require manual algebra or reading of the full paper.
```

---

## 3. Mandatory candidate families

Undermind should not stop after keyword similarity. It should inspect at least these literature families when available:

1. EF21 and error-feedback convergence theory.
2. Communication compression with heterogeneous local objectives.
3. Distributed/federated optimization with worker-specific `L_i`, `mu_i`, or local condition numbers.
4. PEP/interpolation analyses of smooth strongly convex methods.
5. Exact or tight rate/spectral-radius analyses that produce polynomial root conditions.
6. Heterogeneity measures based on variance, dispersion, similarity, dissimilarity, or condition-number mismatch.
7. Results where local functions are scaled versions of one another or share an identical condition ratio.
8. Work on objective similarity, Hessian similarity, local/global condition numbers, or second-order heterogeneity that could be algebraically related even if terminology differs.

---

## 4. Evidence extraction table

For every candidate retained after abstract screening, record the following fields:

```text
candidate_id
citation
identifier
url
publication_year
venue
paper_family
exact_location
local_Li_heterogeneity        yes/no/unclear
local_mui_heterogeneity       yes/no/unclear
both_Li_and_mui               yes/no/unclear
fixed_average_conditioning    yes/no/unclear
heterogeneity_measure
algebraic_mapping_to_K1K2
aligned_invariance_overlap
root_sensitivity_overlap
cubic_root_structure_overlap
classification                A/B/C/D
confidence                    high/medium/low
novelty_threat                critical/material/minor/none
notes
```

A candidate must not receive class `A` solely because it uses words such as “heterogeneity,” “condition number,” “variance,” or “error feedback.” Class `A` requires a demonstrated mathematical equivalence or a result that directly subsumes the claim.

---

## 5. Adjudication rules

### Direct prior art — A

Use only when at least one is true:

- the same expression is present after renaming variables;
- a published theorem directly implies our claim with a short explicit substitution;
- the paper states a more general result from which the claim is an immediate special case;
- the cubic/spectral equation is algebraically identical and the same root property is proved.

### Material overlap — B

Use when the conceptual mechanism is close but at least one substantive mathematical step remains different, for example:

- both `L_i` and `mu_i` are heterogeneous but the proposed measure is not algebraically equivalent;
- proportional heterogeneity is discussed but no invariant cubic/rate result is shown;
- monotonic rate degradation is established with a different heterogeneity quantity;
- a similar polynomial root analysis exists for another compressor or algorithm.

### Adjacent — C

Use for useful context that does not threaten the structural novelty claim.

### Not relevant — D

Use after inspection when apparent keyword overlap does not survive mathematical comparison.

---

## 6. Claim outcomes after Undermind

Each claim N1–N4 should receive one of the following statuses:

```text
CLEAR_TO_PROMOTE
PROMOTE_WITH_PRIOR_ART_POSITIONING
REQUIRES_MANUAL_EQUIVALENCE_CHECK
NOVELTY_CLAIM_MUST_BE_NARROWED
DO_NOT_CLAIM_NOVELTY
```

Do not rewrite the manuscript until every claim has a status and every class-A/B candidate has been manually inspected.

---

## 7. What to bring back from Undermind

Save or paste back:

1. the complete Undermind answer/report;
2. its strongest candidate papers;
3. any PDFs or links for class-A/B candidates;
4. exact theorem/equation/page references;
5. unresolved algebraic equivalence questions.

The next repository phase should then perform a **manual prior-art adjudication**, with the original PDFs checked directly and each equivalence independently verified before the manuscript novelty statement is changed.

---

## 8. OSF remains downstream

OSF is intentionally not part of Phase 14. The archival sequence remains:

1. finish the literature novelty audit;
2. freeze the final claim set;
3. update manuscript/figures/claim registry;
4. run final reproducibility and reviewer audits;
5. create a versioned GitHub release;
6. archive the frozen research package on OSF and obtain the permanent URL/DOI;
7. insert the final OSF and release identifiers into the Data Availability Statement.

This prevents a mutable exploratory state from being mistaken for the final archival record.
