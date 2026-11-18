# Reviewer navigation
1. `data/pilot/stimuli.csv`: inspect 32 texts and factorial construction.
2. `data/pilot/annotations.csv`: inspect 96 ratings; compare IDs and intended/perceived labels.
3. `python scripts/validate.py`: verify coverage, identifiers, ranges, consistency and completeness.
4. `python scripts/analyze.py`: regenerate tables; ranks use integer differences to preserve ties.
5. `python -m pytest -q`: run regression and structural tests.
6. `results/summary.json`: principal numbers and software versions.
7. `results/matched_tests.csv`: canonical and legacy calculations, exact enumerations where specified.
8. `docs/STATISTICAL_REPORTING.md`: manuscript correction audit.
9. `docs/PROVENANCE.md` and `docs/RELEASE_CHECKLIST.md`: what is documented and what requires owner verification.

The package makes the statistical workflow inspectable. It does not certify undisclosed study procedures or remove the four-scenario limitation. The private candidate key and source notes are deliberately not distributed.
