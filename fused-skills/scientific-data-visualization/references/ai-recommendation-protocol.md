# AI multi-dimensional recommendation protocol

Use this protocol after `inspect_data.py` or `route_from_prompt.py`. It guides
recommendation only; it never authorizes fabrication of p-values, confidence
intervals, effect sizes, fitted parameters, prediction metrics, or causal claims.

## Required response contract

State the analytical question first. Then return no more than three chart formats
and no more than three statistical methods, each labelled exactly as:

- **首选**: the task, observed data shape, and all known assumptions match. A method
  with a local adapter also needs an `eligible` packet before it is called verified.
- **待确认候选**: the scientific question matches, but list the smallest missing
  design or data facts before it can become a first choice.
- **不适用**: name the contradiction: outcome type, design, sample support,
  assumptions, or a different scientific question.

For every recommendation, give: data facts used, what it answers, what it does
not answer, required display/diagnostic, and the concrete risk. Do not infer
independence, pairing, experimental unit, causal intent, missingness mechanism,
or a meaningful effect size from column names.

## Chart decision rules

| Task and data facts | First choice | Conditional alternatives | Never default to |
| --- | --- | --- | --- |
| One numeric variable; skew/outliers matter | ECDF or box plot | violin only when sample support reveals shape | mean bar or pie |
| Numeric outcome by groups; small group | individual observations plus box/ECDF | violin when n and density support it | mean-only bar |
| Numeric outcome by groups; n at least 10 each | box plus points | violin plus points, mean bar only for a pre-specified summary | bar hiding raw spread |
| Paired/repeated observations | paired line/slope display | paired scatter | independent-group bar |
| Two numeric variables | scatter | fit only after residual/linearity review | line connecting unordered x |
| Ordered time/process | line | control chart only with at least 20 ordered observations | line over categories |
| Categorical additive burden | Pareto | sorted bar after confirming additivity | pie or unsorted bar |
| Condition matrix/correlation matrix | heatmap with colorbar | faceted heatmap for many panels | rainbow map or 3D surface |

Use data profile flags explicitly: `small_sample`, `strong_skew`,
`iqr_outliers_present`, `substantial_zero_mass`, zero variance, group imbalance,
duplicate rows, correlation summary, time hint, subject-ID hint, and missingness.
If the requested format is reference-only or not in the renderer's 39 supported
core types, identify it as a visual reference rather than a renderable first choice.

## Local strict-adapter methods

The following methods may be called **首选且已验证** only when
`recommend_statistics.py` returns `eligible`: two-sample t/Welch, paired t,
one-/two-/three-way ANOVA, repeated one-way ANOVA, Mann--Whitney,
Kruskal--Wallis, paired Wilcoxon, Friedman, two-sample proportion, logistic and
ordinal regression, Pearson/partial correlation, multiple linear regression,
Kaplan--Meier, Cox, PLS development, discriminant development, K-means,
hierarchical clustering, and supported power calculations. Their existing packet
is authoritative for assumptions, power, leakage, event support, and validation.

## AI conditional-method matrix

The remaining methods below are legitimate **待确认候选** only under their stated
conditions. They remain unverified until an analyst supplies the missing design
facts or a future local adapter is added. The current renderer has 39 supported
core chart types; domain-specific gallery entries remain explicitly
reference-only until their data contracts and renderers are implemented.

| Method | Use when | Ask/inspect before elevating | Do not recommend when |
| --- | --- | --- | --- |
| Column statistics | summarize one or more numeric variables | unit, missingness, mean vs median appropriateness | an inferential comparison is requested |
| Row statistics | repeated measurements within a row have a common scale | row fields represent the same construct and direction | fields are unrelated variables |
| Statistical table | reproducible descriptive summary is the goal | units, grouping, denominator, missing-data rule | it replaces distribution or inference |
| Crosstab/chi-square | association of two categorical variables | expected cell counts, independence, sparse cells, exact alternative | paired/repeated rows or sparse expected counts without an exact plan |
| Discrete frequency | counts of discrete/categorical values | category meaning, denominator, zero category | values are continuous measurements |
| Frequency distribution | describe a continuous distribution | bin sensitivity, sample size, zero inflation, outliers | histogram binning hides small-sample observations |
| Binomial distribution | model successes in fixed independent trials | common success probability, trial count, independence | overdispersion, clustering, unequal trial definition |
| Normality test | assess a continuous residual/sample assumption | n, Q-Q plot, outliers, scientific plausibility | it is used alone to prove normality or select a test mechanically |
| Grubbs outlier test | one suspected error under a normal single-sample model | pre-specified rule, normality, single-outlier premise | repeated deletion, skewed data, or a value is merely inconvenient |
| Dixon Q | one suspected outlier in a genuinely small sample | ordered sample, single-outlier premise, measurement-error rationale | multiple outliers or a non-normal/heterogeneous process |
| One-sample z | compare a mean to a reference with known population variance | known external variance, independent sampling, reference source | variance is estimated from the same sample |
| One-sample variance | compare one normal-population variance to a reference | normality, independent observations, fixed reference | skew/heavy tails or exploratory variance fishing |
| Two-sample variance | compare variability in two independent normal groups | normality, independent groups, robust alternative if violated | using it as a pre-test to choose pooled t |
| One-sample proportion | compare one proportion with a reference | binary definition, independent trials, expected successes/failures, exact plan | clustered trials or sparse counts without exact method |
| Two-way repeated ANOVA | two within-subject factors with continuous response | complete subject-by-cell mapping, sphericity/correction, covariance structure, power | missing cells or unreviewed repeated design |
| One-sample Wilcoxon | one paired-to-reference continuous/ordinal distribution | paired differences, symmetry, zero differences, target location | independent groups or asymmetric differences without a rank interpretation |
| Paired sign test | paired directional change when magnitude assumptions are weak | true pairs, independent pairs, zero-difference handling | unpaired data or an effect-size question needing magnitudes |
| Two-sample KS | compare full continuous distributions | independent groups, continuous/tie handling, question is distribution not only mean | ordinal-heavy ties or only a location question |
| Mood median | compare group medians robustly | independent groups, sufficient counts above/below median | small samples or when distributional power is required |
| PCA | exploratory reduction of correlated numeric variables | scaling, missing-data strategy, sample-to-variable support, stability, loading interpretation | categorical/uncoded fields or confirmation of causal latent factors |
| Weibull fit | parametric survival/reliability shape is scientifically justified | censoring, nonnegative time, shape plausibility, model comparison, validation | arbitrary survival data with no parametric rationale |
| Power one proportion | plan a one-proportion study | reference/target proportions, alpha, sidedness, target power, clustering | post-hoc justification of an already weak study |
| Power one-sample t | plan one mean against a reference | meaningful effect, variance source, alpha, sidedness, target power | variance/effect chosen after inspecting outcomes |
| Power one-way ANOVA | plan multiple independent mean groups | group allocation, Cohen f/means, variance, alpha, target power, multiplicity | repeated/factorial designs or unknown group structure |

## Model-development boundary

PLS, discriminant analysis, clustering, and all regression recommendations grant
only controlled-development eligibility unless a separate training artifact
contains split provenance, preprocessing fit only on training data, tuning rule,
calibration where applicable, uncertainty, and untouched test evaluation. Never
turn an eligibility packet into a performance claim.

## Conditional policy IDs

`column-statistics`, `row-statistics`, `statistical-table`, `crosstab-chi-square`,
`discrete-frequency`, `frequency-distribution`, `binomial-distribution`,
`normality-test`, `grubbs-outlier`, `dixon-q`, `one-sample-z`,
`one-sample-variance`, `two-sample-variance`, `one-sample-proportion`,
`two-way-repeated-anova`, `one-sample-wilcoxon`, `paired-sign`,
`two-sample-ks`, `mood-median`, `pca`, `weibull-fit`,
`power-one-proportion`, `power-one-sample-t`, and `power-one-way-anova`.
