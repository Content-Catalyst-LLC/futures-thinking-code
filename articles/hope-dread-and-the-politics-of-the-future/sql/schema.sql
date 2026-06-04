-- Hope, Dread, and the Politics of the Future schema.
-- SQLite compatible.

DROP VIEW IF EXISTS future_emotion_record_scores;
DROP VIEW IF EXISTS future_emotion_risk_priority_scores;
DROP VIEW IF EXISTS future_emotion_strategy_scores;
DROP VIEW IF EXISTS future_politics_scenario_scores;
DROP VIEW IF EXISTS future_emotion_profile_scores;

DROP TABLE IF EXISTS adaptive_future_emotion_pathways;
DROP TABLE IF EXISTS future_emotion_records;
DROP TABLE IF EXISTS future_emotion_risk_indicators;
DROP TABLE IF EXISTS future_emotion_strategy_options;
DROP TABLE IF EXISTS future_politics_scenarios;
DROP TABLE IF EXISTS future_emotion_profiles;

CREATE TABLE future_emotion_profiles (
    profile_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    hope REAL,
    dread REAL,
    agency REAL,
    trust REAL,
    polarization REAL,
    institutional_capacity REAL,
    future_fatigue REAL,
    narrative_accountability REAL,
    repair_capacity REAL,
    democratic_imagination REAL,
    description TEXT
);

CREATE TABLE future_politics_scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    threat_intensity REAL,
    agency_pathways REAL,
    institutional_trust REAL,
    scapegoating_intensity REAL,
    false_reassurance REAL,
    crisis_fatigue REAL,
    narrative_accountability REAL,
    democratic_participation REAL,
    repair_orientation REAL,
    learning_capacity REAL,
    description TEXT
);

CREATE TABLE future_emotion_strategy_options (
    strategy_id TEXT PRIMARY KEY,
    profile_id TEXT,
    strategy_name TEXT,
    strategy_type TEXT,
    agency_pathway_gain REAL,
    trust_repair_gain REAL,
    narrative_accountability_gain REAL,
    participatory_foresight_gain REAL,
    climate_truth_action_gain REAL,
    youth_representation_gain REAL,
    media_literacy_gain REAL,
    repair_capacity_gain REAL,
    fear_politics_resistance_gain REAL,
    implementation_capacity REAL,
    public_legitimacy_gain REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES future_emotion_profiles(profile_id)
);

CREATE TABLE future_emotion_risk_indicators (
    risk_id TEXT PRIMARY KEY,
    scenario_id TEXT,
    risk_name TEXT,
    risk_domain TEXT,
    probability_proxy REAL,
    severity REAL,
    irreversibility REAL,
    visibility_gap REAL,
    distributional_harm REAL,
    democratic_harm REAL,
    preparedness REAL,
    description TEXT,
    FOREIGN KEY(scenario_id) REFERENCES future_politics_scenarios(scenario_id)
);

CREATE TABLE future_emotion_records (
    record_id TEXT PRIMARY KEY,
    profile_id TEXT,
    record_name TEXT,
    hope REAL,
    dread REAL,
    agency REAL,
    trust REAL,
    future_fatigue REAL,
    repair_capacity REAL,
    polarization REAL,
    narrative_accountability REAL,
    description TEXT,
    FOREIGN KEY(profile_id) REFERENCES future_emotion_profiles(profile_id)
);

CREATE TABLE adaptive_future_emotion_pathways (
    pathway_id TEXT PRIMARY KEY,
    profile_id TEXT,
    scenario_id TEXT,
    pathway_name TEXT,
    hope REAL,
    dread REAL,
    agency REAL,
    trust REAL,
    future_fatigue REAL,
    repair_capacity REAL,
    polarization REAL,
    narrative_accountability REAL,
    time_horizon INTEGER,
    FOREIGN KEY(profile_id) REFERENCES future_emotion_profiles(profile_id),
    FOREIGN KEY(scenario_id) REFERENCES future_politics_scenarios(scenario_id)
);

CREATE VIEW future_emotion_profile_scores AS
SELECT
    profile_id,
    scenario_name,
    scenario_family,
    ROUND(agency * (hope + 0.55 * dread) * trust, 4) AS mobilization_score,
    ROUND(dread * (1 - agency) * (1 - trust), 4) AS paralysis_risk_score,
    ROUND(
      0.18 * hope +
      0.18 * agency +
      0.16 * trust +
      0.16 * institutional_capacity +
      0.14 * narrative_accountability +
      0.12 * repair_capacity -
      0.04 * future_fatigue -
      0.02 * polarization,
      4
    ) AS disciplined_hope_score,
    ROUND(
      0.24 * dread +
      0.22 * polarization +
      0.18 * (1 - trust) +
      0.16 * (1 - agency) +
      0.12 * future_fatigue +
      0.08 * (1 - narrative_accountability),
      4
    ) AS fear_politics_risk_score
FROM future_emotion_profiles;

CREATE VIEW future_politics_scenario_scores AS
SELECT
    scenario_id,
    scenario_name,
    scenario_family,
    ROUND(
      0.14 * threat_intensity +
      0.12 * (1 - agency_pathways) +
      0.12 * (1 - institutional_trust) +
      0.14 * scapegoating_intensity +
      0.12 * false_reassurance +
      0.12 * crisis_fatigue +
      0.09 * (1 - narrative_accountability) +
      0.07 * (1 - democratic_participation) +
      0.05 * (1 - repair_orientation) +
      0.03 * (1 - learning_capacity),
      4
    ) AS future_politics_risk_score
FROM future_politics_scenarios;

CREATE VIEW future_emotion_strategy_scores AS
SELECT
    strategy_id,
    profile_id,
    strategy_name,
    strategy_type,
    ROUND(
      0.13 * agency_pathway_gain +
      0.12 * trust_repair_gain +
      0.13 * narrative_accountability_gain +
      0.11 * participatory_foresight_gain +
      0.11 * climate_truth_action_gain +
      0.10 * youth_representation_gain +
      0.08 * media_literacy_gain +
      0.10 * repair_capacity_gain +
      0.08 * fear_politics_resistance_gain +
      0.02 * implementation_capacity +
      0.02 * public_legitimacy_gain,
      4
    ) AS future_emotion_strategy_value_score
FROM future_emotion_strategy_options;

CREATE VIEW future_emotion_risk_priority_scores AS
SELECT
    risk_id,
    scenario_id,
    risk_name,
    risk_domain,
    ROUND(
      0.14 * probability_proxy +
      0.16 * severity +
      0.12 * irreversibility +
      0.12 * visibility_gap +
      0.16 * distributional_harm +
      0.20 * democratic_harm +
      0.10 * (1 - preparedness),
      4
    ) AS future_emotion_risk_priority_score
FROM future_emotion_risk_indicators;

CREATE VIEW future_emotion_record_scores AS
SELECT
    record_id,
    profile_id,
    record_name,
    ROUND(agency * (hope + 0.55 * dread) * trust, 4) AS mobilization_score,
    ROUND(dread * (1 - agency) * (1 - trust), 4) AS paralysis_risk_score,
    ROUND(
      0.22 * hope +
      0.22 * agency +
      0.18 * trust +
      0.18 * repair_capacity +
      0.12 * narrative_accountability -
      0.05 * future_fatigue -
      0.03 * polarization,
      4
    ) AS disciplined_hope_score,
    ROUND(
      CASE
        WHEN hope - narrative_accountability - repair_capacity > 0
        THEN hope - narrative_accountability - repair_capacity
        ELSE 0
      END,
      4
    ) AS false_hope_risk_score
FROM future_emotion_records;
