# Reproducibility Notes

Default workflow:

```bash
python3 python/technology_foresight_workflow.py
```

Advanced workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-advanced.txt
python python/technology_foresight_advanced.py
```

Smoke test:

```bash
bash run_smoke_tests.sh
```
