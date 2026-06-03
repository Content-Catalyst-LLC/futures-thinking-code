# Reproducibility Notes

## Default Workflow

The main Python workflow uses only the Python standard library.

```bash
python3 python/business_strategy_futures_workflow.py
```

## Advanced Workflow

The advanced workflow uses pandas, numpy, and matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/business_strategy_futures_advanced.py
```

## Smoke Test

```bash
bash run_smoke_tests.sh
```

Generated outputs are written to `outputs/`.

## Reproducibility Principle

Every output should be traceable to strategy profiles, scenario records, strategic options, capability records, early-warning indicators, pathway parameters, and code.
