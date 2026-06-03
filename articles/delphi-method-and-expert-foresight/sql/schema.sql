-- Delphi Method and Expert Foresight schema.
-- SQLite compatible.

DROP VIEW IF EXISTS foresight_translation_register;
DROP VIEW IF EXISTS rationale_theme_counts;
DROP VIEW IF EXISTS issue_priority_scores;
DROP VIEW IF EXISTS delphi_round_metrics;
DROP VIEW IF EXISTS expert_judgment_profiles;
DROP VIEW IF EXISTS panel_diversity_audit;

DROP TABLE IF EXISTS foresight_outputs;
DROP TABLE IF EXISTS qualitative_rationales;
DROP TABLE IF EXISTS issue_priorities;
DROP TABLE IF EXISTS delphi_responses;
DROP TABLE IF EXISTS expert_panel;

CREATE TABLE expert_panel (
    expert_id TEXT PRIMARY KEY,
    expertise_domain TEXT NOT NULL,
    sector TEXT,
    formal_expert TEXT,
    practice_expert TEXT,
    community_expert TEXT,
    ethics_expert TEXT,
    years_experience INTEGER,
    panel_weight REAL,
    blind_spot_risk REAL,
    description TEXT
);

CREATE TABLE delphi_responses (
    response_id TEXT PRIMARY KEY,
    expert_id TEXT,
    round INTEGER,
    issue_id TEXT,
    issue_title TEXT,
    likelihood REAL,
    impact REAL,
    urgency REAL,
    feasibility REAL,
    confidence REAL,
    low_estimate REAL,
    high_estimate REAL,
    rationale_code TEXT,
    FOREIGN KEY(expert_id) REFERENCES expert_panel(expert_id)
);

CREATE TABLE issue_priorities (
    issue_id TEXT PRIMARY KEY,
    issue_title TEXT NOT NULL,
    domain TEXT,
    likelihood REAL,
    impact REAL,
    uncertainty REAL,
    urgency REAL,
    governance_relevance REAL,
    monitoring_need REAL,
    description TEXT
);

CREATE TABLE qualitative_rationales (
    rationale_code TEXT PRIMARY KEY,
    theme TEXT,
    interpretive_summary TEXT,
    decision_implication TEXT
);

CREATE TABLE foresight_outputs (
    output_id TEXT PRIMARY KEY,
    issue_id TEXT,
    output_type TEXT,
    output_title TEXT,
    decision_use TEXT,
    monitoring_indicator TEXT,
    review_frequency TEXT,
    FOREIGN KEY(issue_id) REFERENCES issue_priorities(issue_id)
);

CREATE VIEW panel_diversity_audit AS
SELECT
    expert_id,
    expertise_domain,
    sector,
    panel_weight,
    blind_spot_risk,
    ROUND(
      (
        (CASE WHEN lower(formal_expert) = 'true' THEN 1.0 ELSE 0.0 END) +
        (CASE WHEN lower(practice_expert) = 'true' THEN 1.0 ELSE 0.0 END) +
        (CASE WHEN lower(community_expert) = 'true' THEN 1.0 ELSE 0.0 END) +
        (CASE WHEN lower(ethics_expert) = 'true' THEN 1.0 ELSE 0.0 END)
      ) / 4.0 * panel_weight * (1 - blind_spot_risk),
      4
    ) AS panel_diversity_score
FROM expert_panel;

CREATE VIEW expert_judgment_profiles AS
SELECT
    response_id,
    expert_id,
    round,
    issue_id,
    issue_title,
    ROUND(
      0.25 * likelihood +
      0.35 * impact +
      0.25 * urgency +
      0.15 * feasibility,
      4
    ) AS judgment_profile,
    ROUND(high_estimate - low_estimate, 4) AS uncertainty_range,
    rationale_code
FROM delphi_responses;

CREATE VIEW delphi_round_metrics AS
SELECT
    issue_id,
    round,
    COUNT(*) AS respondent_count,
    ROUND(AVG(
      0.25 * likelihood +
      0.35 * impact +
      0.25 * urgency +
      0.15 * feasibility
    ), 4) AS mean_judgment_profile,
    ROUND(AVG(high_estimate - low_estimate), 4) AS mean_uncertainty_range,
    ROUND(AVG(likelihood), 4) AS mean_likelihood,
    ROUND(AVG(impact), 4) AS mean_impact,
    ROUND(AVG(urgency), 4) AS mean_urgency
FROM delphi_responses
GROUP BY issue_id, round;

CREATE VIEW issue_priority_scores AS
SELECT
    issue_id,
    issue_title,
    domain,
    ROUND(
      0.25 * likelihood +
      0.30 * impact +
      0.20 * urgency +
      0.15 * governance_relevance +
      0.10 * monitoring_need,
      4
    ) AS priority_score,
    ROUND(
      (
        0.25 * likelihood +
        0.30 * impact +
        0.20 * urgency +
        0.15 * governance_relevance +
        0.10 * monitoring_need
      ) * (1 + 0.20 * uncertainty),
      4
    ) AS uncertainty_adjusted_priority
FROM issue_priorities;

CREATE VIEW rationale_theme_counts AS
SELECT
    r.rationale_code,
    q.theme,
    COUNT(*) AS response_count,
    q.decision_implication
FROM delphi_responses r
JOIN qualitative_rationales q ON r.rationale_code = q.rationale_code
GROUP BY r.rationale_code, q.theme, q.decision_implication;

CREATE VIEW foresight_translation_register AS
SELECT
    output_id,
    issue_id,
    output_type,
    output_title,
    decision_use,
    monitoring_indicator,
    review_frequency
FROM foresight_outputs;
