(* EF21 symbolic cross-checks for the controlled two-agent study. *)

ClearAll[
  FixedAverageMus, CubicIngredients, CubicPolynomial, CubicCoefficients,
  EmpiricalEtaStar, HomogeneousEtaStar, HomogeneousRate,
  NumericRhoStar, RetainedMargin, SymbolicReport
];

FixedAverageMus[tau_, muBar_] := {
  2 muBar/(1 + tau),
  2 muBar tau/(1 + tau)
};

CubicIngredients[tau_, epsilon_, L_: 1, muBar_: 1/10] := Module[
  {s, r, mus, sigma, delta, k1, k2},
  s = Sqrt[epsilon];
  r = (1 - s)^2/(1 + s);
  mus = FixedAverageMus[tau, muBar];
  sigma = {L, L} + mus;
  delta = {L, L} - mus;
  k1 = (delta[[2]]^2 sigma[[1]] + delta[[1]]^2 sigma[[2]])/
    (sigma[[1]] sigma[[2]] Total[sigma]);
  k2 = Total[delta]^2/Total[sigma]^2;
  <|"s" -> s, "r" -> r, "mu1" -> mus[[1]], "mu2" -> mus[[2]],
    "K1" -> FullSimplify[k1], "K2" -> FullSimplify[k2]|>
];

CubicPolynomial[rho_, tau_, epsilon_, L_: 1, muBar_: 1/10] := Module[
  {x, s, r, k1, k2},
  x = CubicIngredients[tau, epsilon, L, muBar];
  {s, r, k1, k2} = Lookup[x, {"s", "r", "K1", "K2"}];
  Expand[
    rho^3 - (s (2 + s) + r (s k1 + k2)) rho^2 +
    s^2 (1 + 2 s + r (k1 + s k2)) rho - s^4
  ]
];

CubicCoefficients[tau_, epsilon_, L_: 1, muBar_: 1/10] :=
  CoefficientList[CubicPolynomial[rho, tau, epsilon, L, muBar], rho] // Reverse;

EmpiricalEtaStar[tau_, epsilon_, L_: 1, muBar_: 1/10] := Module[
  {mus = FixedAverageMus[tau, muBar], s = Sqrt[epsilon]},
  4/(2 L + Total[mus]) (1 - s)/(1 + s)
];

HomogeneousEtaStar[epsilon_, L_: 1, mu_: 1/10] :=
  2/(L + mu) (1 - Sqrt[epsilon])/(1 + Sqrt[epsilon]);

HomogeneousRate[epsilon_, L_: 1, mu_: 1/10] := Module[
  {s = Sqrt[epsilon], kappa, psi},
  If[TrueQ[FullSimplify[L == mu]], Return[s]];
  kappa = L/mu;
  psi = 1 - s + Sqrt[(1 + s)^2 + s 16 kappa/(kappa - 1)^2];
  s + (1 - s)/2 ((kappa - 1)/(kappa + 1))^2 psi
];

NumericRhoStar[tau_?NumericQ, epsilon_?NumericQ, L_: 1., muBar_: .1] := Module[
  {roots, realRoots},
  roots = rho /. NRoots[CubicPolynomial[rho, tau, epsilon, L, muBar] == 0, rho];
  realRoots = Select[roots, Abs[Im[N[#]]] < 10^-10 && -10^-10 <= Re[N[#]] <= 1 + 10^-10 &];
  If[realRoots === {}, Indeterminate, Max[Re[N[realRoots]]]]
];

RetainedMargin[tau_?NumericQ, epsilon_?NumericQ, L_: 1., muBar_: .1] := Module[
  {rho = NumericRhoStar[tau, epsilon, L, muBar], rhoH = N[HomogeneousRate[epsilon, L, muBar]]},
  (1 - rho)/(1 - rhoH)
];

SymbolicReport[] := Module[
  {assumptions, scaleCheck, etaCheck, homogeneousK},
  assumptions = 0 < tau <= 1 && 0 < epsilon < 1 && L > 0 && 0 < muBar <= L && c > 0;
  scaleCheck = FullSimplify[
    CubicCoefficients[tau, epsilon, c L, c muBar] - CubicCoefficients[tau, epsilon, L, muBar],
    assumptions
  ];
  etaCheck = FullSimplify[
    EmpiricalEtaStar[1, epsilon, L, muBar] - HomogeneousEtaStar[epsilon, L, muBar],
    assumptions
  ];
  homogeneousK = FullSimplify[
    Lookup[CubicIngredients[1, epsilon, L, muBar], {"K1", "K2"}],
    assumptions
  ];
  <|
    "scale_invariance_coefficient_difference" -> scaleCheck,
    "homogeneous_eta_difference" -> etaCheck,
    "homogeneous_K1_K2" -> homogeneousK,
    "discriminant" -> Factor[Discriminant[CubicPolynomial[rho, tau, epsilon, L, muBar], rho]]
  |>
];
