(* Phase 13 — full-heterogeneity symbolic root-structure audit
   This script treats Empirical Law 4.3 as an inherited cubic object.
   It proves conditional algebraic/root-structure consequences of that cubic;
   it does not prove Empirical Law 4.3 as an EF21 convergence theorem. *)

ClearAll[
  k, tauL, tauMu, L1, L2, mu1, mu2, sigma1, sigma2, delta1, delta2,
  K1, K2, gap, gapClosed, s, rho, r, Q, disc, assumptions,
  dQdK1, dQdrho
];

(* Scale-normalized fixed-average parameterization: Lbar=1, mubar=1/k. *)
L1 = 2/(1 + tauL);
L2 = 2 tauL/(1 + tauL);
mu1 = 2/(k (1 + tauMu));
mu2 = 2 tauMu/(k (1 + tauMu));

sigma1 = FullSimplify[L1 + mu1];
sigma2 = FullSimplify[L2 + mu2];
delta1 = FullSimplify[L1 - mu1];
delta2 = FullSimplify[L2 - mu2];

K1 = FullSimplify[
  (delta2^2 sigma1 + delta1^2 sigma2)/
    (sigma1 sigma2 (sigma1 + sigma2)),
  Assumptions -> {k > 1, 0 < tauL <= 1, 0 < tauMu <= 1}
];

K2 = FullSimplify[
  (delta1 + delta2)^2/(sigma1 + sigma2)^2,
  Assumptions -> {k > 1, 0 < tauL <= 1, 0 < tauMu <= 1}
];

gap = Factor@FullSimplify[
  K1 - K2,
  Assumptions -> {k > 1, 0 < tauL <= 1, 0 < tauMu <= 1}
];

gapClosed =
  4 k^2 (tauL - tauMu)^2/
   ((k + 1)^2
     (tauL + k tauMu + k + 1)
     (k tauL tauMu + tauL tauMu + k tauL + tauMu));

structureCertificate = <|
  "K2Invariant" -> FullSimplify[
    K2 == ((k - 1)/(k + 1))^2,
    Assumptions -> {k > 1, 0 < tauL <= 1, 0 < tauMu <= 1}
  ],
  "MismatchClosedForm" -> FullSimplify[
    gap == gapClosed,
    Assumptions -> {k > 1, 0 < tauL <= 1, 0 < tauMu <= 1}
  ],
  "Worker1Margin" -> Factor[delta1],
  "Worker2Margin" -> Factor[delta2]
|>;

(* Generic cubic coordinates. Under positive local regularity,
   q_i=(L_i-mu_i)/(L_i+mu_i) lies in [0,1), so weighted-moment structure gives
   0 <= K2 <= K1 < 1. For k>1, K2>0. *)
r = (1 - s)^2/(1 + s);
Q = rho^3
  - (s (2 + s) + r (s K1 + K2)) rho^2
  + s^2 (1 + 2 s + r (K1 + s K2)) rho
  - s^4;

disc = Together[Discriminant[Q, rho]];
dQdK1 = Factor[D[Q, K1]];
dQdrho = Factor[D[Q, rho]];

assumptions = 0 < s < 1 && 0 < K2 < 1 && K2 <= K1 < 1;

rootCertificate = <|
  "DiscriminantNonpositiveFeasible" ->
    Reduce[assumptions && disc <= 0, {s, K1, K2}, Reals],
  "NonpositiveRootFeasible" ->
    Reduce[assumptions && rho <= 0 && Q == 0, {s, K1, K2, rho}, Reals],
  "RootAtOrAboveOneFeasible" ->
    Reduce[assumptions && rho >= 1 && Q == 0, {s, K1, K2, rho}, Reals],
  "QAtS" -> Factor[Q /. rho -> s],
  "QAtOne" -> Factor[Q /. rho -> 1],
  "QAtOneNonpositiveFeasible" ->
    Reduce[assumptions && (Q /. rho -> 1) <= 0, {s, K1, K2}, Reals],
  "dQdK1" -> dQdK1,
  "ImplicitDerivative" -> Factor[-dQdK1/dQdrho]
|>;

Print["Phase 13 structure certificate:"];
Print[structureCertificate];
Print["Phase 13 generic root certificate:"];
Print[rootCertificate];

(* Interpretation:
   - DiscriminantNonpositiveFeasible == False implies three distinct real roots.
   - NonpositiveRootFeasible == False and RootAtOrAboveOneFeasible == False put
     all three roots in (0,1).
   - Q(s)=K2 (s-1)^3 s^2 < 0 and Q(1)>0, so at least one root lies in (s,1);
     hence the largest root rhoStar satisfies rhoStar>s.
   - For a monic cubic with three simple real roots, Q'(rhoStar)>0 at the
     largest root.
   - d rhoStar/dK1 = r s rhoStar (rhoStar-s)/Q'(rhoStar) > 0.
   - Since K1>=K2 and equality holds exactly for tauL=tauMu, the inherited
     largest-root contraction factor is minimized on the aligned path.
*)
