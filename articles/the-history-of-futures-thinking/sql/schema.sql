-- The History of Futures Thinking schema.
-- SQLite compatible.

DROP TABLE IF EXISTS historical_risks;
DROP TABLE IF EXISTS timeline_periods;
DROP TABLE IF EXISTS method_genealogy;
DROP TABLE IF EXISTS institutional_developments;
DROP TABLE IF EXISTS historical_traditions;

CREATE TABLE historical_traditions (
    tradition_id TEXT PRIMARY KEY,
    tradition TEXT NOT NULL,
    period TEXT,
    methodological_discipline REAL CHECK (methodological_discipline >= 0 AND methodological_discipline <= 1),
    institutional_power REAL CHECK (institutional_power >= 0 AND institutional_power <= 1),
    participatory_depth REAL CHECK (participatory_depth >= 0 AND participatory_depth <= 1),
    ethical_reflection REAL CHECK (ethical_reflection >= 0 AND ethical_reflection <= 1),
    systems_orientation REAL CHECK (systems_orientation >= 0 AND systems_orientation <= 1),
    description TEXT
);

CREATE TABLE institutional_developments (
    institution_id TEXT PRIMARY KEY,
    institution_or_development TEXT NOT NULL,
    year INTEGER,
    domain TEXT,
    significance TEXT,
    method_influence REAL CHECK (method_influence >= 0 AND method_influence <= 1),
    public_accountability REAL CHECK (public_accountability >= 0 AND public_accountability <= 1)
);

CREATE TABLE method_genealogy (
    method_id TEXT PRIMARY KEY,
    method TEXT NOT NULL,
    origin_tradition TEXT,
    primary_use TEXT,
    participatory_potential REAL CHECK (participatory_potential >= 0 AND participatory_potential <= 1),
    technocratic_risk REAL CHECK (technocratic_risk >= 0 AND technocratic_risk <= 1),
    ethical_sensitivity REAL CHECK (ethical_sensitivity >= 0 AND ethical_sensitivity <= 1)
);

CREATE TABLE timeline_periods (
    period_id TEXT PRIMARY KEY,
    period TEXT NOT NULL,
    approx_start INTEGER,
    approx_end INTEGER,
    dominant_future_logic TEXT,
    key_development TEXT,
    ethical_risk TEXT
);

CREATE TABLE historical_risks (
    risk_id TEXT PRIMARY KEY,
    risk_name TEXT NOT NULL,
    description TEXT,
    affected_traditions TEXT,
    severity REAL CHECK (severity >= 0 AND severity <= 1),
    mitigation_priority TEXT
);

CREATE VIEW historical_tradition_scores AS
SELECT
    tradition_id,
    tradition,
    ROUND(
      0.25 * methodological_discipline +
      0.25 * participatory_depth +
      0.25 * ethical_reflection +
      0.25 * systems_orientation,
      4
    ) AS reflective_foresight_score,
    ROUND(
      institutional_power *
      (1 - participatory_depth) *
      (1 - ethical_reflection),
      4
    ) AS power_risk_score
FROM historical_traditions;

CREATE VIEW method_genealogy_scores AS
SELECT
    method_id,
    method,
    origin_tradition,
    ROUND(
      technocratic_risk *
      (1 - participatory_potential) *
      (1 - ethical_sensitivity),
      4
    ) AS method_risk_score,
    ROUND(
      0.34 * participatory_potential +
      0.33 * ethical_sensitivity +
      0.33 * (1 - technocratic_risk),
      4
    ) AS reflective_method_score
FROM method_genealogy;
