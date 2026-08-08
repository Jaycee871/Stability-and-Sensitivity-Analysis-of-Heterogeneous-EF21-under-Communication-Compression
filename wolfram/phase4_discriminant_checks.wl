(* Phase 4 symbolic structure checks for the controlled EF21 cubic. *)

ClearAll[Phase4DiscriminantCheck, Phase4ScaleCheck];

Phase4DiscriminantCheck[kappa_] := Module[
  {m, L, mu1, mu2, sigma1, sigma2, delta1, delta2, k1, k2, r, q,
   disc, reduced, poly, coeffs},
  m = 1/kappa;
  L = 1;
  mu1 = 2 m/(1 + tau);
  mu2 = 2 m tau/(1 + tau);
  sigma1 = L + mu1;
  sigma2 = L + mu2;
  delta1 = L - mu1;
  delta2 = L - mu2;
  k1 = Together[(delta2^2 sigma1 + delta1^2 sigma2)/
    (sigma1 sigma2 (sigma1 + sigma2))];
  k2 = Together[(delta1 + delta2)^2/(sigma1 + sigma2)^2];
  r = (1 - s)^2/(1 + s);
  q = x^3 - (s (2 + s) + r (s k1 + k2)) x^2 +
    s^2 (1 + 2 s + r (k1 + s k2)) x - s^4;
  disc = Factor[Together[Discriminant[q, x]]];
  reduced = Together[disc/((1 - s)^6 s^4)];
  poly = Numerator[reduced];
  coeffs = Last /@ CoefficientRules[poly, {s, tau}];
  <|
    "kappa_bar" -> kappa,
    "strictly_positive_polynomial_coefficients" -> And @@ Thread[coeffs > 0],
    "coefficient_count" -> Length[coeffs],
    "minimum_coefficient" -> Min[coeffs],
    "discriminant_positive_on_open_domain" ->
      (And @@ Thread[coeffs > 0])
  |>
];

Phase4ScaleCheck[] := Module[
  {mu1, mu2, sigma1, sigma2, delta1, delta2, k1, k2,
   mu1c, mu2c, sigma1c, sigma2c, delta1c, delta2c, k1c, k2c},
  mu1 = 2 m/(1 + tau);
  mu2 = 2 m tau/(1 + tau);
  sigma1 = L + mu1;
  sigma2 = L + mu2;
  delta1 = L - mu1;
  delta2 = L - mu2;
  k1 = (delta2^2 sigma1 + delta1^2 sigma2)/
    (sigma1 sigma2 (sigma1 + sigma2));
  k2 = (delta1 + delta2)^2/(sigma1 + sigma2)^2;

  mu1c = 2 c m/(1 + tau);
  mu2c = 2 c m tau/(1 + tau);
  sigma1c = c L + mu1c;
  sigma2c = c L + mu2c;
  delta1c = c L - mu1c;
  delta2c = c L - mu2c;
  k1c = (delta2c^2 sigma1c + delta1c^2 sigma2c)/
    (sigma1c sigma2c (sigma1c + sigma2c));
  k2c = (delta1c + delta2c)^2/(sigma1c + sigma2c)^2;

  FullSimplify[
    {k1c - k1, k2c - k2},
    0 < tau <= 1 && L > 0 && m > 0 && c > 0
  ]
];

report = <|
  "engine" -> $Version,
  "scale_invariance_K1_K2_difference" -> Phase4ScaleCheck[],
  "strata" -> (Phase4DiscriminantCheck /@ {2, 10, 100})
|>;

Print[report];
