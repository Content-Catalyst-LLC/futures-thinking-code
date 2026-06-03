# Validation Checklist

Use this checklist before publishing or extending the workflow.

- [ ] All required directories exist.
- [ ] Default Python workflow runs without external packages.
- [ ] Outputs are generated in `outputs/`.
- [ ] SQL schema loads in SQLite if available.
- [ ] Advanced Python workflow fails gracefully if dependencies are missing.
- [ ] Data dictionary matches CSV columns.
- [ ] Assumption vulnerability scores are interpretable.
- [ ] Scenario robustness rankings are plausible.
- [ ] Regret analysis identifies brittle strategies.
- [ ] README contains the GitHub directory URL.
