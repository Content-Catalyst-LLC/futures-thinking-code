-- The Future of Work and Automation schema.
-- SQLite compatible.

DROP VIEW IF EXISTS strategy_option_scores;
DROP VIEW IF EXISTS social_protection_scores;
DROP VIEW IF EXISTS algorithmic_management_risk_scores;
DROP VIEW IF EXISTS work_scenario_scores;
DROP VIEW IF EXISTS task_exposure_scores;
DROP VIEW IF EXISTS occupation_future_scores;

DROP TABLE IF EXISTS strategy_options;
DROP TABLE IF EXISTS pathway_parameters;
DROP TABLE IF EXISTS social_protection_indicators;
DROP TABLE IF EXISTS algorithmic_management_risks;
DROP TABLE IF EXISTS work_scenarios;
DROP TABLE IF EXISTS task_exposure_matrix;
DROP TABLE IF EXISTS occupation_profiles;

CREATE TABLE occupation_profiles (
    occupation_id TEXT PRIMARY KEY,
    occupation_name TEXT NOT NULL,
    sector TEXT,
    employment_scale REAL,
    wage_security REAL,
    task_exposure REAL,
    augmentation_capacity REAL,
    worker_voice REAL,
    training_access REAL,
    social_protection REAL,
    surveillance_intensity REAL,
    initial_job_quality REAL,
    description TEXT
);

CREATE TABLE task_exposure_matrix (
    task_id TEXT PRIMARY KEY,
    occupation_id TEXT,
    task_name TEXT,
    task_category TEXT,
    task_weight REAL,
    ai_exposure REAL,
    robotics_exposure REAL,
    monitoring_exposure REAL,
    augmentation_potential REAL,
    human_context_requirement REAL,
    description TEXT,
    FOREIGN KEY(occupation_id) REFERENCES occupation_profiles(occupation_id)
);

CREATE TABLE work_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT,
    scenario_family TEXT,
    automation_intensity REAL,
    augmentation_capacity REAL,
    worker_voice REAL,
    job_quality REAL,
    surveillance_intensity REAL,
    transition_support REAL,
    skill_mobility REAL,
    social_protection REAL,
    description TEXT
);

CREATE TABLE algorithmic_management_risks (
    risk_id TEXT PRIMARY KEY,
    occupation_id TEXT,
    risk_name TEXT,
    risk_type TEXT,
    probability REAL,
    severity REAL,
    detection_difficulty REAL,
    worker_voice_gap REAL,
    due_process_gap REAL,
    privacy_exposure REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(occupation_id) REFERENCES occupation_profiles(occupation_id)
);

CREATE TABLE social_protection_indicators (
    protection_id TEXT PRIMARY KEY,
    occupation_id TEXT,
    protection_name TEXT,
    training_access REAL,
    income_support REAL,
    portable_benefits REAL,
    wage_floor REAL,
    appeal_rights REAL,
    collective_bargaining_access REAL,
    public_investment REAL,
    description TEXT,
    FOREIGN KEY(occupation_id) REFERENCES occupation_profiles(occupation_id)
);

CREATE TABLE pathway_parameters (
    pathway_id TEXT PRIMARY KEY,
    occupation_id TEXT,
    pathway_name TEXT,
    task_exposure REAL,
    augmentation_capacity REAL,
    worker_voice REAL,
    training_access REAL,
    social_protection REAL,
    surveillance_intensity REAL,
    initial_job_quality REAL,
    time_horizon INTEGER,
    FOREIGN KEY(occupation_id) REFERENCES occupation_profiles(occupation_id)
);

CREATE TABLE strategy_options (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT,
    strategy_type TEXT,
    automation_governance REAL,
    worker_voice REAL,
    training_commitment REAL,
    social_protection REAL,
    job_quality_commitment REAL,
    privacy_protection REAL,
    productivity_sharing REAL,
    care_investment REAL,
    description TEXT
);

CREATE VIEW occupation_future_scores AS
SELECT
    occupation_id,
    occupation_name,
    sector,
    ROUND(
      0.34 * task_exposure +
      0.22 * surveillance_intensity +
      0.18 * (1 - worker_voice) +
      0.14 * (1 - training_access) +
      0.12 * (1 - social_protection),
      4
    ) AS exposure_pressure_score,
    ROUND(
      0.20 * augmentation_capacity +
      0.20 * worker_voice +
      0.16 * training_access +
      0.16 * social_protection +
      0.14 * wage_security +
      0.14 * (1 - surveillance_intensity),
      4
    ) AS worker_centered_capacity_score,
    ROUND(
      task_exposure * (1 - training_access) * (1 - social_protection + surveillance_intensity / 2),
      4
    ) AS transition_risk_score
FROM occupation_profiles;

CREATE VIEW task_exposure_scores AS
SELECT
    task_id,
    occupation_id,
    task_name,
    task_category,
    ROUND(task_weight * (
      0.42 * ai_exposure +
      0.28 * robotics_exposure +
      0.18 * monitoring_exposure +
      0.12 * (1 - human_context_requirement)
    ), 4) AS weighted_automation_exposure,
    ROUND(task_weight * (
      0.60 * augmentation_potential +
      0.25 * human_context_requirement +
      0.15 * ai_exposure
    ), 4) AS weighted_augmentation_score
FROM task_exposure_matrix;

CREATE VIEW work_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.18 * augmentation_capacity +
      0.18 * worker_voice +
      0.18 * job_quality +
      0.14 * transition_support +
      0.14 * skill_mobility +
      0.12 * social_protection +
      0.06 * (1 - surveillance_intensity),
      4
    ) AS worker_centered_capacity_score,
    ROUND(
      0.30 * automation_intensity +
      0.22 * surveillance_intensity +
      0.18 * (1 - transition_support) +
      0.16 * (1 - skill_mobility) +
      0.14 * (1 - social_protection),
      4
    ) AS displacement_control_pressure_score
FROM work_scenarios;

CREATE VIEW algorithmic_management_risk_scores AS
SELECT
    risk_id,
    occupation_id,
    risk_name,
    risk_type,
    ROUND(
      0.18 * probability +
      0.20 * severity +
      0.14 * detection_difficulty +
      0.16 * worker_voice_gap +
      0.16 * due_process_gap +
      0.10 * privacy_exposure +
      0.06 * (1 - mitigation_capacity),
      4
    ) AS algorithmic_management_risk_score,
    mitigation_capacity
FROM algorithmic_management_risks;

CREATE VIEW social_protection_scores AS
SELECT
    protection_id,
    occupation_id,
    protection_name,
    ROUND(
      0.16 * training_access +
      0.16 * income_support +
      0.14 * portable_benefits +
      0.14 * wage_floor +
      0.14 * appeal_rights +
      0.14 * collective_bargaining_access +
      0.12 * public_investment,
      4
    ) AS social_protection_readiness_score,
    ROUND(
      1 - (
        0.16 * training_access +
        0.16 * income_support +
        0.14 * portable_benefits +
        0.14 * wage_floor +
        0.14 * appeal_rights +
        0.14 * collective_bargaining_access +
        0.12 * public_investment
      ),
      4
    ) AS social_protection_gap_score
FROM social_protection_indicators;

CREATE VIEW strategy_option_scores AS
SELECT
    strategy_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.16 * automation_governance +
      0.18 * worker_voice +
      0.14 * training_commitment +
      0.14 * social_protection +
      0.14 * job_quality_commitment +
      0.10 * privacy_protection +
      0.08 * productivity_sharing +
      0.06 * care_investment,
      4
    ) AS worker_centered_strategy_score,
    ROUND(
      0.14 * worker_voice +
      0.14 * social_protection +
      0.14 * job_quality_commitment +
      0.16 * productivity_sharing +
      0.14 * care_investment +
      0.14 * training_commitment +
      0.14 * automation_governance,
      4
    ) AS shared_prosperity_score
FROM strategy_options;
