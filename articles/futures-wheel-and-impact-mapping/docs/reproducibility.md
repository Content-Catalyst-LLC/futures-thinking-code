# Reproducibility Notes

## Default Workflow

The main Python workflow uses only the Python standard library.

```bash
python3 python/futures_wheel_workflow.py
```

## Advanced Workflow

The advanced workflow uses pandas and matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/futures_wheel_advanced.py
```

## Smoke Test

```bash
bash run_smoke_tests.sh
```

Generated outputs are written to `outputs/`.
