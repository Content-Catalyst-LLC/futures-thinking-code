# Reproducibility Notes

## Default Workflow

The main Python workflow uses only the Python standard library.

```bash
python3 python/societal_transformation_workflow.py
```

## Advanced Workflow

The advanced workflow uses pandas, numpy, and matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/societal_transformation_advanced.py
```

## Smoke Test

```bash
bash run_smoke_tests.sh
```

Generated outputs are written to `outputs/`.

## Reproducibility Principle

Every output should be traceable to drivers, weak signals, scenario profiles, system-pressure indicators, equity indicators, pathway parameters, strategy assumptions, and code.
