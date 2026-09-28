# Cover letter draft

Dear Editors of *Mathematics*,

Please consider our manuscript, **“Sensitivity of Two-Agent Error Feedback 21 to Heterogeneous Regularity under Compression,”** for publication as an Article in the Special Issue **“Artificial Intelligence and Algorithms.”**

The manuscript examines the two-agent heterogeneous cubic relation reported as Empirical Law 4.3 in *A Tight Theory of Error Feedback Algorithms in Distributed Optimization*. We independently reproduced the relation across the complete 10,500-configuration source grid and assessed numerical consistency through polynomial residuals, agreement with the homogeneous theoretical limit, comparison with the reference implementation, and negative controls.

Building on this numerical reproduction, the study analyzes how communication compression interacts with heterogeneous local regularity. The equal smoothness analysis evaluates 216,027 controlled configurations. The full regularity analysis then allows local smoothness and strong convexity to vary independently while their arithmetic means remain fixed. In this parameterization, the empirical step size and the average regularity coefficient remain invariant, and the remaining dependence reduces to the nonnegative mismatch measure $\Psi=K_1-K_2$, equal to the weighted variance of local regularity ratios. Proportional variation produces zero mismatch even when the agents remain heterogeneous. Symbolic analysis further shows that, conditional on the reproduced cubic relation and for positive compression error, the selected contraction root increases with mismatch.

The manuscript maintains a strict scope distinction throughout. It does not present the inherited empirical relation as a newly proved general EF$^{21}$ convergence theorem. Instead, it provides a reproducible numerical, algebraic, and symbolic characterization of the relation in the stated two-agent setting.

The repository containing the analysis code, numerical summaries, symbolic verification materials, and reproducibility scripts is publicly available at:

https://github.com/Jaycee871/Stability-and-Sensitivity-Analysis-of-Heterogeneous-EF21-under-Communication-Compression

We believe the manuscript is appropriate for the Special Issue because it combines distributed optimization, communication compression, numerical reproduction, symbolic analysis, and sensitivity analysis.

We confirm that the manuscript is not under consideration by another journal and has not been published previously in journal form. All authors will approve the submitted version and accept responsibility for the work.

**Editorial independence.** Fu-Hsing Wang is a co-author and corresponding author of this manuscript, serves as a Guest Editor of the Special Issue “Artificial Intelligence and Algorithms,” and is the academic advisor of Pack Kwan Low. We respectfully request that the manuscript be handled by an independent Editorial Board Member or another Academic Editor without a conflict of interest. Fu-Hsing Wang should have no role in reviewer selection or the editorial decision for this submission.

Thank you for your consideration.

Sincerely,

**Fu-Hsing Wang**  
Corresponding Author  
Department of Information Management, Chinese Culture University  
55 Hwa-Kang Rd., Yang-Ming-Shan, Taipei 11114, Taiwan  
wfx2@ulive.pccu.edu.tw
