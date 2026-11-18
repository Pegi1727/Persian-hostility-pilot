# Statistical reporting audit and correction notice

## Why some earlier values changed
Previous manuscript calculations used differences of binary floating-point means. For example, mathematically equal absolute differences of one third can be represented as 0.3333333333333339 and 0.33333333333333304. Ranking these as different breaks genuine ties. Earlier review also incorrectly endorsed p = .063 as an exact tied-rank result. That endorsement is corrected here.

The canonical implementation ranks differences of integer sums of the three ratings. These are exactly three times the differences in item means, so the statistical information is unchanged while genuine ties are preserved. Means, SDs, ICC, kappas, classification counts, and target percentages are unchanged.

| Comparison | Earlier manuscript | Correct tied-rank calculation |
|---|---|---|
| Hostility manipulation | W = 0; approx p ≈ .000429 (incorrectly labelled exact originally) | W = 0; normal p ≈ .000412; report p < .001 |
| Arousal manipulation | W = 0; approx p ≈ .000418 (incorrectly labelled exact originally) | W = 0; normal p ≈ .000398; report p < .001 |
| Arousal effect on hostility, intended absent | W = 0; exact p = .008 | W = 0; exact p = .0078125; report .008 |
| Arousal effect on hostility, intended present | W = 1; p = .063 | W = 1.50; exact p = .09375; report .094 |
| Naturalness, present minus absent hostility | W = 32.50; p = .606 | W = 31.00; normal p ≈ .523003; report .523 |
| Naturalness, high minus low arousal | W = 31.00; p = .304 | W = 29.50; normal p ≈ .253098; report .253 |

The intended-present arousal contrast has sum-differences +3, +1, 0, +3, −1, 0, +3, +5 (order is immaterial). The two absolute differences of 1 receive average rank 1.5. The three absolute differences of 3 receive average rank 4; the absolute difference of 5 receives rank 6. Therefore W− = 1.5 and two-sided exact enumeration gives 6/64 = .09375. A unit test checks this case explicitly.

## Manuscript replacements
Section 4.5: “When hostility was intended to be present, the corresponding mean difference was 0.58 points (SD = 0.68; eight matched contrasts). Two zero differences were excluded. An exact sign-permutation calculation preserving tied absolute differences yielded W = 1.50, p = .094.”

Section 4.8, hostility: replace W = 32.50, p = .606 with **W = 31.00, p = .523**.

Section 4.8, arousal: replace W = 31.00, p = .304 with **W = 29.50, p = .253**.

Section 3.6: explicitly state that rank inputs were integer differences in three-rater rating sums, a positive rescaling of item-mean differences that preserves mathematical ties.

No substantive inference becomes confirmatory. Exact sign enumeration does not address shared-scenario dependence. The pilot remains exploratory; no interaction or naturalness equivalence is established.

`results/matched_tests.csv` exposes both canonical results and a legacy floating-point normal-approximation sensitivity calculation. Canonical results, not legacy artifacts, should be used in the final manuscript.
