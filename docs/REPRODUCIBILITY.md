# Reproducibility record
The package was executed locally with Python 3.11, NumPy 1.26.4, pandas 2.2.2, SciPy 1.13.1, scikit-learn 1.5.1, and pytest 8.2.2. Exact Python patch version is recorded in results/summary.json.

Nine tests passed locally. The local hosted environment required disabling unrelated preinstalled pytest plugins:
```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q
```
A clean virtual environment with only requirements.txt installed should not have those unrelated plugins. GitHub Actions is provided but has not been run remotely: local execution is not a claim of successful GitHub-hosted CI.

Static-file integrity covers code, data, configuration, and documentation, not regenerated results, interpreter versions, file timestamps, or the manifest itself. Checksums detect changes, not scientific validity, rights clearance, consent, or authenticity.
