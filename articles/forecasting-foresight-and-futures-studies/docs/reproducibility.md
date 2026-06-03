# Reproducibility Notes

## Default Workflow

The main Python workflow uses only the Python standard library.

Run:

```bash
python3 python/futures_research_workflow.py
```

## Advanced Workflow

The advanced workflow uses pandas and matplotlib.

Run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/futures_research_workflow_advanced.py
```

## Outputs

Generated outputs are written to `outputs/`.

## Validation

The smoke test runs the default Python workflow and then runs optional language examples only if the relevant compilers or runtimes are available.
