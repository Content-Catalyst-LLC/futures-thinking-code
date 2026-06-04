# Reproducibility Notes

## Default Workflow

The main Python workflow uses only the Python standard library.

```bash
python3 python/planetary_boundaries_workflow.py
```

## Advanced Workflow

The advanced workflow uses pandas, numpy, and matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/planetary_boundaries_workflow_advanced.py
```

## Smoke Test

```bash
bash run_smoke_tests.sh
```

Generated outputs are written to `outputs/`.

## Reproducibility Principle

Every output should be traceable to pathway profiles, scenarios, strategy options, risk indicators, governance records, simulation parameters, and code.
