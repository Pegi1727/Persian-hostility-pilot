# Data dictionary
All CSV files use UTF-8; empty cells represent unavailable values, not zero. Persian text must not be normalized or translated silently.

## annotations.csv (96 rows)
| Field | Meaning |
|---|---|
| public_item_id | Pilot item ID, PIL-001 through PIL-032 |
| annotator_id | Pseudonymous ANN-01, ANN-02, ANN-03 |
| guideline_version, stimulus_version | Original metadata: pilot-0.3 |
| scenario_id | Four pilot scenario identifiers |
| policy_stance_intended | support / opposition; design label |
| hostility_intended | absent / present; design label |
| arousal_intended | low / high; design label |
| policy_stance_perceived | support / opposition / mixed / unclear |
| hostility_1to7 | Perceived hostility, integer 1–7 |
| hostility_confidence_1to7 | Confidence, integer 1–7; not used as a weight |
| arousal_1to7 | Perceived emotional intensity, integer 1–7 |
| naturalness_1to7 | Perceived naturalness, integer 1–7 |
| hostility_expression | explicit / implicit / not_applicable / unclear |
| target_status | identified / no_evaluation / unclear |
| target_policy, target_group, target_individual, target_other | Binary selections when available; multiple selections possible |

Higher numeric ratings indicate more of the named attribute. Exact scale-anchor wording is not reconstructed from the numeric data and must be supplied from the actual guideline. Group targeting is not equivalent to hostility.

## stimuli.csv (32 rows)
One row per stimulus, including context, text, scenario, and intended factor labels. This file is explicitly **unblinded** and is for reproducibility, not for recruiting a new blinded annotation cohort.

Supplementary valence measures were collected in the original forms but are not part of the analyses reproduced here; they are omitted from this minimized release. Their omission is not evidence that all supplementary fields were complete.
