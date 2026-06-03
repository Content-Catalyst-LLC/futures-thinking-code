-- Causal Layered Analysis schema.
-- SQLite compatible.

DROP VIEW IF EXISTS scenario_translation_register;
DROP VIEW IF EXISTS power_legitimacy_audit_scores;
DROP VIEW IF EXISTS reframing_depth_scores;
DROP VIEW IF EXISTS metaphor_reframing_scores;
DROP VIEW IF EXISTS layer_transformation_priorities;
DROP VIEW IF EXISTS cla_issue_depth_scores;

DROP TABLE IF EXISTS scenario_translation;
DROP TABLE IF EXISTS power_audit;
DROP TABLE IF EXISTS reframing_profiles;
DROP TABLE IF EXISTS metaphor_map;
DROP TABLE IF EXISTS layer_codes;
DROP TABLE IF EXISTS cla_issues;

CREATE TABLE cla_issues (
    issue_id TEXT PRIMARY KEY,
    issue_title TEXT NOT NULL,
    domain TEXT,
    time_horizon INTEGER,
    litany_visibility REAL,
    systemic_explanation REAL,
    worldview_challenge REAL,
    myth_metaphor_depth REAL,
    reframing_potential REAL,
    power_sensitivity REAL,
    strategic_relevance REAL,
    description TEXT
);

CREATE TABLE layer_codes (
    code_id TEXT PRIMARY KEY,
    issue_id TEXT,
    layer_level INTEGER,
    layer_label TEXT,
    statement TEXT,
    diagnostic_weight REAL,
    transformation_need REAL,
    notes TEXT,
    FOREIGN KEY(issue_id) REFERENCES cla_issues(issue_id)
);

CREATE TABLE metaphor_map (
    metaphor_id TEXT PRIMARY KEY,
    issue_id TEXT,
    dominant_metaphor TEXT,
    alternative_metaphor TEXT,
    dominant_effect TEXT,
    alternative_effect TEXT,
    metaphor_shift_score REAL,
    ethical_relevance REAL,
    FOREIGN KEY(issue_id) REFERENCES cla_issues(issue_id)
);

CREATE TABLE reframing_profiles (
    reframe_id TEXT PRIMARY KEY,
    issue_id TEXT,
    old_litany TEXT,
    new_litany TEXT,
    old_worldview TEXT,
    new_worldview TEXT,
    old_metaphor TEXT,
    new_metaphor TEXT,
    litany_change REAL,
    systemic_change REAL,
    worldview_change REAL,
    metaphor_change REAL,
    power_awareness REAL,
    strategic_coherence REAL,
    FOREIGN KEY(issue_id) REFERENCES cla_issues(issue_id)
);

CREATE TABLE power_audit (
    audit_id TEXT PRIMARY KEY,
    issue_id TEXT,
    dominant_voice TEXT,
    excluded_voice TEXT,
    power_risk REAL,
    exclusion_risk REAL,
    legitimacy_need REAL,
    counter_narrative TEXT,
    FOREIGN KEY(issue_id) REFERENCES cla_issues(issue_id)
);

CREATE TABLE scenario_translation (
    scenario_id TEXT PRIMARY KEY,
    issue_id TEXT,
    reframed_scenario TEXT,
    scenario_logic TEXT,
    backcasting_target TEXT,
    monitoring_indicator TEXT,
    review_frequency TEXT,
    FOREIGN KEY(issue_id) REFERENCES cla_issues(issue_id)
);

CREATE VIEW cla_issue_depth_scores AS
SELECT
    issue_id,
    issue_title,
    domain,
    ROUND(
      0.10 * litany_visibility +
      0.18 * systemic_explanation +
      0.22 * worldview_challenge +
      0.20 * myth_metaphor_depth +
      0.16 * reframing_potential +
      0.08 * power_sensitivity +
      0.06 * strategic_relevance,
      4
    ) AS cla_depth_score
FROM cla_issues;

CREATE VIEW layer_transformation_priorities AS
SELECT
    code_id,
    issue_id,
    layer_level,
    layer_label,
    statement,
    ROUND(diagnostic_weight * transformation_need, 4) AS layer_priority
FROM layer_codes;

CREATE VIEW metaphor_reframing_scores AS
SELECT
    metaphor_id,
    issue_id,
    dominant_metaphor,
    alternative_metaphor,
    ROUND(0.60 * metaphor_shift_score + 0.40 * ethical_relevance, 4) AS metaphor_reframing_score
FROM metaphor_map;

CREATE VIEW reframing_depth_scores AS
SELECT
    reframe_id,
    issue_id,
    old_metaphor,
    new_metaphor,
    ROUND(
      0.12 * litany_change +
      0.20 * systemic_change +
      0.22 * worldview_change +
      0.22 * metaphor_change +
      0.12 * power_awareness +
      0.12 * strategic_coherence,
      4
    ) AS reframing_depth_score
FROM reframing_profiles;

CREATE VIEW power_legitimacy_audit_scores AS
SELECT
    audit_id,
    issue_id,
    dominant_voice,
    excluded_voice,
    ROUND(0.40 * power_risk + 0.30 * exclusion_risk + 0.30 * legitimacy_need, 4) AS power_legitimacy_score,
    counter_narrative
FROM power_audit;

CREATE VIEW scenario_translation_register AS
SELECT
    scenario_id,
    issue_id,
    reframed_scenario,
    scenario_logic,
    backcasting_target,
    monitoring_indicator,
    review_frequency
FROM scenario_translation;
