-- Backcasting and Strategic Planning schema.
-- SQLite compatible.

DROP VIEW IF EXISTS scenario_stress_burdens;
DROP VIEW IF EXISTS constraint_priorities;
DROP VIEW IF EXISTS milestone_risk_priorities;
DROP VIEW IF EXISTS pathway_viability_scores;
DROP VIEW IF EXISTS strategic_gap_scores;

DROP TABLE IF EXISTS scenario_stress_tests;
DROP TABLE IF EXISTS monitoring_triggers;
DROP TABLE IF EXISTS constraints;
DROP TABLE IF EXISTS milestones;
DROP TABLE IF EXISTS pathways;
DROP TABLE IF EXISTS current_baselines;
DROP TABLE IF EXISTS desired_futures;

CREATE TABLE desired_futures (
    future_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    domain TEXT,
    target_year INTEGER,
    decarbonization REAL,
    equity REAL,
    resilience REAL,
    institutional_capacity REAL,
    public_legitimacy REAL,
    ecological_integrity REAL,
    description TEXT
);

CREATE TABLE current_baselines (
    future_id TEXT PRIMARY KEY,
    current_decarbonization REAL,
    current_equity REAL,
    current_resilience REAL,
    current_institutional_capacity REAL,
    current_public_legitimacy REAL,
    current_ecological_integrity REAL,
    baseline_note TEXT,
    FOREIGN KEY(future_id) REFERENCES desired_futures(future_id)
);

CREATE TABLE pathways (
    pathway_id TEXT PRIMARY KEY,
    future_id TEXT,
    pathway_name TEXT NOT NULL,
    feasibility REAL,
    institutional_difficulty REAL,
    transition_speed REAL,
    stakeholder_alignment REAL,
    resilience REAL,
    justice REAL,
    adaptability REAL,
    political_friction REAL,
    description TEXT,
    FOREIGN KEY(future_id) REFERENCES desired_futures(future_id)
);

CREATE TABLE milestones (
    milestone_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    phase_year INTEGER,
    milestone TEXT NOT NULL,
    dependency TEXT,
    completion_score REAL,
    risk_score REAL,
    owner_role TEXT,
    FOREIGN KEY(pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE constraints (
    constraint_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    constraint_type TEXT,
    constraint_description TEXT NOT NULL,
    impact REAL,
    severity REAL,
    reversibility REAL,
    mitigation TEXT,
    FOREIGN KEY(pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE monitoring_triggers (
    trigger_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    indicator TEXT NOT NULL,
    threshold REAL,
    review_frequency TEXT,
    trigger_action TEXT,
    FOREIGN KEY(pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE scenario_stress_tests (
    stress_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    scenario_name TEXT,
    climate_stress REAL,
    political_resistance REAL,
    funding_constraint REAL,
    technology_uncertainty REAL,
    public_trust REAL,
    stress_note TEXT,
    FOREIGN KEY(pathway_id) REFERENCES pathways(pathway_id)
);

CREATE VIEW strategic_gap_scores AS
SELECT
    f.future_id,
    f.future_name,
    f.domain,
    f.target_year,
    ROUND(
      (
        (f.decarbonization - b.current_decarbonization) +
        (f.equity - b.current_equity) +
        (f.resilience - b.current_resilience) +
        (f.institutional_capacity - b.current_institutional_capacity) +
        (f.public_legitimacy - b.current_public_legitimacy) +
        (f.ecological_integrity - b.current_ecological_integrity)
      ) / 6.0,
      4
    ) AS strategic_gap_score
FROM desired_futures f
JOIN current_baselines b ON f.future_id = b.future_id;

CREATE VIEW pathway_viability_scores AS
SELECT
    pathway_id,
    future_id,
    pathway_name,
    ROUND(
      0.18 * feasibility -
      0.16 * institutional_difficulty +
      0.14 * transition_speed +
      0.18 * stakeholder_alignment +
      0.16 * resilience +
      0.12 * justice +
      0.14 * adaptability -
      0.12 * political_friction,
      4
    ) AS pathway_viability_score
FROM pathways;

CREATE VIEW milestone_risk_priorities AS
SELECT
    milestone_id,
    pathway_id,
    phase_year,
    milestone,
    ROUND(risk_score * (1 - completion_score), 4) AS milestone_risk_priority,
    owner_role
FROM milestones;

CREATE VIEW constraint_priorities AS
SELECT
    constraint_id,
    pathway_id,
    constraint_type,
    constraint_description,
    ROUND(impact * severity * (1 + (1 - reversibility)), 4) AS constraint_priority,
    mitigation
FROM constraints;

CREATE VIEW scenario_stress_burdens AS
SELECT
    stress_id,
    pathway_id,
    scenario_name,
    ROUND(
      0.22 * climate_stress +
      0.20 * political_resistance +
      0.20 * funding_constraint +
      0.18 * technology_uncertainty +
      0.20 * (1 - public_trust),
      4
    ) AS stress_burden_score
FROM scenario_stress_tests;
