-- Ethics of Futures Thinking schema.
-- SQLite compatible.

DROP VIEW IF EXISTS stakeholder_distribution_scores;
DROP VIEW IF EXISTS ethical_risk_priority_scores;
DROP VIEW IF EXISTS ethical_strategy_scores;
DROP VIEW IF EXISTS ethical_scenario_scores;
DROP VIEW IF EXISTS ethical_futures_profile_scores;

DROP TABLE IF EXISTS intergenerational_ethics_pathways;
DROP TABLE IF EXISTS stakeholder_distribution_paths;
DROP TABLE IF EXISTS ethical_risk_indicators;
DROP TABLE IF EXISTS ethical_strategy_options;
DROP TABLE IF EXISTS ethical_futures_scenarios;
DROP TABLE IF EXISTS ethical_futures_profiles;

CREATE TABLE ethical_futures_profiles (
    profile_id TEXT PRIMARY KEY,
    institution_type TEXT NOT NULL,
    profile_family TEXT,
    intergenerational_responsibility REAL,
    inclusion REAL,
    accountability REAL,
    risk_equity REAL,
    transparency REAL,
    contestability REAL,
    precaution REAL,
    adaptive_learning REAL,
    epistemic_pluralism REAL,
    public_legitimacy REAL,
    description TEXT
);

CREATE TABLE ethical_futures_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    technocratic_opacity REAL,
    participation_depth REAL,
    intergenerational_weight REAL,
    risk_inequality REAL,
    corporate_capture_pressure REAL,
    security_drift REAL,
    climate_justice_alignment REAL,
    ai_opacity REAL,
    accountability_strength REAL,
    adaptive_learning_capacity REAL,
    description TEXT
);

CREATE TABLE ethical_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    value_transparency_gain REAL,
    participation_gain REAL,
    distributional_justice_gain REAL,
    intergenerational_review_gain REAL,
    epistemic_pluralism_gain REAL,
    precaution_gain REAL,
    accountability_gain REAL,
    contestability_gain REAL,
    adaptive_learning_gain REAL,
    implementation_capacity REAL,
    public_legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES ethical_futures_profiles(profile_id)
);

CREATE TABLE ethical_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    visibility_gap REAL,
    distributional_harm REAL,
    rights_risk REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES ethical_futures_scenarios(scenario_id)
);

CREATE TABLE stakeholder_distribution_paths (
    record_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    group_name TEXT,
    time_period INTEGER,
    benefit REAL,
    risk REAL,
    voice_weight REAL,
    moral_weight REAL,
    exposure REAL,
    protection REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES ethical_futures_scenarios(scenario_id)
);

CREATE TABLE intergenerational_ethics_pathways (
    pathway_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    pathway_name TEXT,
    present_benefit REAL,
    future_benefit REAL,
    present_risk REAL,
    future_risk REAL,
    discount_weight REAL,
    inequality_penalty REAL,
    participation_quality REAL,
    accountability_strength REAL,
    precaution_strength REAL,
    adaptive_learning_capacity REAL,
    time_horizon INTEGER,
    FOREIGN KEY(scenario_id) REFERENCES ethical_futures_scenarios(scenario_id)
);

CREATE VIEW ethical_futures_profile_scores AS
SELECT
    profile_id,
    institution_type,
    profile_family,
    ROUND(
      0.13 * intergenerational_responsibility +
      0.12 * inclusion +
      0.12 * accountability +
      0.12 * risk_equity +
      0.10 * transparency +
      0.10 * contestability +
      0.10 * precaution +
      0.08 * adaptive_learning +
      0.08 * epistemic_pluralism +
      0.05 * public_legitimacy,
      4
    ) AS ethical_futures_profile_score
FROM ethical_futures_profiles;

CREATE VIEW ethical_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.14 * technocratic_opacity +
      0.14 * risk_inequality +
      0.12 * corporate_capture_pressure +
      0.12 * security_drift +
      0.12 * ai_opacity +
      0.10 * (1 - participation_depth) +
      0.10 * (1 - intergenerational_weight) +
      0.08 * (1 - accountability_strength) +
      0.04 * (1 - climate_justice_alignment) +
      0.04 * (1 - adaptive_learning_capacity),
      4
    ) AS ethical_failure_risk_score
FROM ethical_futures_scenarios;

CREATE VIEW ethical_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.11 * value_transparency_gain +
      0.13 * participation_gain +
      0.13 * distributional_justice_gain +
      0.12 * intergenerational_review_gain +
      0.10 * epistemic_pluralism_gain +
      0.09 * precaution_gain +
      0.11 * accountability_gain +
      0.10 * contestability_gain +
      0.07 * adaptive_learning_gain +
      0.02 * implementation_capacity +
      0.02 * public_legitimacy_gain,
      4
    ) AS ethical_strategy_value_score
FROM ethical_strategy_options;

CREATE VIEW ethical_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.17 * severity +
      0.15 * irreversibility +
      0.10 * visibility_gap +
      0.20 * distributional_harm +
      0.14 * rights_risk +
      0.10 * (1 - preparedness),
      4
    ) AS ethical_risk_priority_score
FROM ethical_risk_indicators;

CREATE VIEW stakeholder_distribution_scores AS
SELECT
    record_id,
    scenario_id,
    group_name,
    time_period,
    ROUND(benefit - risk, 4) AS net_welfare,
    ROUND(
      benefit - risk - 0.35 * exposure + 0.25 * protection + 0.20 * moral_weight + 0.10 * voice_weight,
      4
    ) AS justice_adjusted_score,
    ROUND(
      CASE WHEN exposure > protection THEN exposure - protection ELSE 0 END,
      4
    ) AS vulnerability_gap
FROM stakeholder_distribution_paths;
