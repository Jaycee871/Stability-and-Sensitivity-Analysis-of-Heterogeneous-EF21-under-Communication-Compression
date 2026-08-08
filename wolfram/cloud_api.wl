(*
  Restricted Wolfram Cloud API for EF21 symbolic/numeric cross-checks.
  It does NOT evaluate arbitrary user-supplied Wolfram expressions.

  Run after evaluating ef21_symbolic.wl in the same Wolfram Cloud session.
  Change $EF21APIPermissions to "Public" only if you intentionally want a
  read-only public endpoint that an external client can query.
*)

ClearAll[EF21APIResponse, $EF21APIPermissions];
$EF21APIPermissions = "Private";

EF21APIResponse[action_String, tau_?NumericQ, epsilon_?NumericQ, kappa_?NumericQ] := Module[
  {muBar, coeffs, rho, rhoH, result},
  If[!(0 < tau <= 1 && 0 < epsilon < 1 && kappa >= 1),
    Return[<|"ok" -> False, "error" -> "Require 0<tau<=1, 0<epsilon<1, kappa>=1."|>]
  ];
  muBar = 1/kappa;
  result = Switch[action,
    "coefficients",
      coeffs = N[CubicCoefficients[tau, epsilon, 1, muBar], 16];
      <|"coefficients" -> coeffs|>,
    "roots",
      <|"rho_star" -> N[NumericRhoStar[tau, epsilon, 1., N[muBar]], 16]|>,
    "retention",
      rho = NumericRhoStar[tau, epsilon, 1., N[muBar]];
      rhoH = N[HomogeneousRate[epsilon, 1, muBar], 16];
      <|"rho_star" -> rho, "rho_homogeneous" -> rhoH,
        "retained_margin" -> N[(1 - rho)/(1 - rhoH), 16]|>,
    "discriminant",
      <|"discriminant" -> N[
        Discriminant[CubicPolynomial[x, tau, epsilon, 1, muBar], x], 16
      ]|>,
    _,
      Return[<|"ok" -> False,
        "error" -> "Unknown action. Use coefficients, roots, retention, or discriminant."|>]
  ];
  Join[<|"ok" -> True, "action" -> action, "tau" -> N[tau],
    "epsilon" -> N[epsilon], "kappa_bar" -> N[kappa]|>, result]
];

EF21CloudAPI = APIFunction[
  {
    "action" -> "String",
    "tau" -> "Number",
    "epsilon" -> "Number",
    "kappa" -> "Number"
  },
  EF21APIResponse[#action, #tau, #epsilon, #kappa] &,
  "JSON"
];

(* Example deployment. Choose your own CloudObject path if desired. *)
EF21CloudObject = CloudDeploy[
  EF21CloudAPI,
  CloudObject["ef21-symbolic-api"],
  Permissions -> $EF21APIPermissions
];

EF21CloudObject
