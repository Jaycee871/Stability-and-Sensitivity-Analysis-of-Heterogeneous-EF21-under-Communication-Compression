(* Export deterministic Wolfram results for cross-checking against Python. *)

scriptDir = DirectoryName[$InputFileName];
Get[FileNameJoin[{scriptDir, "ef21_symbolic.wl"}]];

input = Import[FileNameJoin[{scriptDir, "reference_cases.json"}], "RawJSON"];
cases = Lookup[input, "cases"];

results = Map[
  Function[case,
    Module[{tau, epsilon, kappa, muBar, coeffs, rho, rhoH, retention},
      tau = Lookup[case, "tau"];
      epsilon = Lookup[case, "epsilon"];
      kappa = Lookup[case, "kappa_bar"];
      muBar = 1/kappa;
      coeffs = N[CubicCoefficients[tau, epsilon, 1, muBar], 17];
      rho = N[NumericRhoStar[tau, epsilon, 1., N[muBar]], 17];
      rhoH = N[HomogeneousRate[epsilon, 1, muBar], 17];
      retention = N[(1 - rho)/(1 - rhoH), 17];
      <|
        "tau" -> N[tau, 17],
        "epsilon" -> N[epsilon, 17],
        "kappa_bar" -> N[kappa, 17],
        "coefficients" -> coeffs,
        "rho_star" -> rho,
        "rho_homogeneous" -> rhoH,
        "retained_margin" -> retention,
        "discriminant" -> N[
          Discriminant[CubicPolynomial[x, tau, epsilon, 1, muBar], x], 17
        ]
      |>
    ]
  ],
  cases
];

report = <|
  "engine" -> "Wolfram Language",
  "version" -> $Version,
  "symbolic_report" -> Map[ToString[InputForm[#]] &, SymbolicReport[]],
  "cases" -> results
|>;

outputDir = FileNameJoin[{scriptDir, "outputs"}];
If[!DirectoryQ[outputDir], CreateDirectory[outputDir]];
outputPath = FileNameJoin[{outputDir, "wolfram_reference.json"}];
Export[outputPath, report, "RawJSON"];
Print["Wrote ", outputPath];
