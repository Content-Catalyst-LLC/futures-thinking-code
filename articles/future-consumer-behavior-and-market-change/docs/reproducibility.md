# Reproducibility Notes

## Default Workflow

The main Python workflow uses only the Python standard library.

```bash
python3 python/consumer_market_futures_workflow.py
```

## Advanced Workflow

The advanced workflow uses pandas numpy and matplotlib.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/consumer_market_futures_advanced.py
```

## Smoke Test

```bash
bash run_smoke_tests.sh
```

Generated outputs are written to `outputs/`.

## Reproducibility Principle

Every output should be traceable to consumer profiles market scenarios strategy options vulnerability records regulatory records adoption-pathway parameters and code.
