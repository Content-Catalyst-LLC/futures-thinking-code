# Methodology

This companion repository treats the future of work and automation as a task-level, occupation-level, and institution-level transformation problem.

## Core Analytical Tasks

1. Validate occupation, task, scenario, risk, protection, pathway, and strategy records.
2. Score occupation exposure, job quality, worker-centered capacity, and transition risk.
3. Score task exposure using task weights, AI exposure, robotics exposure, monitoring exposure, augmentation potential, and human-context requirements.
4. Score scenario worker-centered capacity and displacement/control pressure.
5. Score algorithmic management risks.
6. Score social protection readiness.
7. Simulate job quality, transition risk, and skill mobility over time.
8. Score strategy options for worker-centered automation governance.
9. Export reproducible tables and a report.

## Core Equations

### Occupation Exposure

`exposure = 0.34 × task_exposure + 0.22 × surveillance_intensity + 0.18 × (1 - worker_voice) + 0.14 × (1 - training_access) + 0.12 × (1 - social_protection)`

### Worker-Centered Capacity

`capacity = 0.18 × augmentation_capacity + 0.18 × worker_voice + 0.18 × job_quality + 0.14 × transition_support + 0.14 × skill_mobility + 0.12 × social_protection + 0.06 × (1 - surveillance_intensity)`

### Transition Risk

`risk = task_exposure × (1 - training_access) × (1 - social_protection + surveillance_intensity / 2)`

### Job Quality

`quality = wage_security + worker_voice + training_access + social_protection - surveillance_intensity`

### Social Protection Readiness

`readiness = 0.16 × training_access + 0.16 × income_support + 0.14 × portable_benefits + 0.14 × wage_floor + 0.14 × appeal_rights + 0.14 × collective_bargaining_access + 0.12 × public_investment`

## Interpretation

Scores are not predictions. They are structured prompts for comparing occupations, tasks, risks, worker voice, social protection, job quality, and alternative automation pathways.
