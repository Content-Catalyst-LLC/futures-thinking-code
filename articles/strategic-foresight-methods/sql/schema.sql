-- Strategic Foresight Methods schema.
-- SQLite compatible.

DROP TABLE IF EXISTS strategy_translation;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS drivers_uncertainties;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS pipeline_profiles;
DROP TABLE IF EXISTS foresight_methods;

CREATE TABLE foresight_methods (
    method_id TEXT PRIMARY KEY,
    method TEXT NOT NULL,
    primary_function TEXT,
    detection_power REAL CHECK (detection_power >= 0 AND detection_power <= 1),
    ambiguity_tolerance REAL CHECK (ambiguity_tolerance >= 0 AND ambiguity_tolerance <= 1),
    structural_depth REAL CHECK (structural_depth >= 0 AND structural_depth <= 1),
    actionability REAL CHECK (actionability >= 0 AND actionability <= 1),
    participatory_depth REAL CHECK (participatory_depth >= 0 AND participatory_depth <= 1),
    institutional_fit REAL CHECK (institutional_fit >= 0 AND institutional_fit <= 1),
    learning_value REAL CHECK (learning_value >= 0 AND learning_value <= 1),
    technocratic_risk REAL CHECK (technocratic_risk >= 0 AND technocratic_risk <= 1)
);

CREATE TABLE pipeline_profiles (
    pipeline_id TEXT PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    detection REAL,
    interpretation REAL,
    pattern_formation REAL,
    uncertainty_structuring REAL,
    strategic_design REAL,
    legitimacy REAL,
    uptake REAL,
    resistance REAL
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    domain TEXT,
    signal TEXT NOT NULL,
    uncertainty REAL,
    impact REAL,
    novelty REAL,
    source_type TEXT,
    monitoring_priority TEXT
);

CREATE TABLE drivers_uncertainties (
    driver_id TEXT PRIMARY KEY,
    domain TEXT,
    driver_or_uncertainty TEXT NOT NULL,
    driver_type TEXT,
    uncertainty REAL,
    impact REAL,
    velocity REAL,
    description TEXT
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    domain TEXT,
    confidence REAL,
    exposure REAL,
    reversibility REAL,
    monitoring_signal TEXT
);

CREATE TABLE strategy_translation (
    insight_id TEXT PRIMARY KEY,
    foresight_insight TEXT NOT NULL,
    decision_area TEXT,
    action_option TEXT,
    monitoring_indicator TEXT,
    review_frequency TEXT,
    decision_linkage REAL
);

CREATE VIEW foresight_method_profile_scores AS
SELECT
    method_id,
    method,
    primary_function,
    ROUND(
      0.16 * detection_power +
      0.14 * ambiguity_tolerance +
      0.16 * structural_depth +
      0.18 * actionability +
      0.14 * participatory_depth +
      0.10 * institutional_fit +
      0.12 * learning_value,
      4
    ) AS method_profile_score,
    ROUND(
      technocratic_risk * (1 - participatory_depth) * (1 - learning_value),
      4
    ) AS method_risk_score
FROM foresight_methods;

CREATE VIEW signal_watch_scores AS
SELECT
    signal_id,
    domain,
    signal,
    ROUND(0.35 * uncertainty + 0.40 * impact + 0.25 * novelty, 4) AS watch_score,
    monitoring_priority
FROM signals;

CREATE VIEW driver_criticality_scores AS
SELECT
    driver_id,
    domain,
    driver_or_uncertainty,
    driver_type,
    ROUND(uncertainty * impact * velocity, 4) AS criticality_score
FROM drivers_uncertainties;

CREATE VIEW assumption_vulnerability_scores AS
SELECT
    assumption_id,
    domain,
    assumption_text,
    ROUND(exposure * (1 - confidence) * (1 + (1 - reversibility)), 4) AS vulnerability_score,
    monitoring_signal
FROM assumptions;
