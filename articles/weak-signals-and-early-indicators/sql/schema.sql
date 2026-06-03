-- Weak Signals and Early Indicators schema.
-- SQLite compatible.

DROP TABLE IF EXISTS watchlist;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS propagation_pathways;
DROP TABLE IF EXISTS signal_clusters;
DROP TABLE IF EXISTS early_indicators;
DROP TABLE IF EXISTS weak_signals;

CREATE TABLE weak_signals (
    signal_id TEXT PRIMARY KEY,
    signal_title TEXT NOT NULL,
    domain TEXT,
    signal_type TEXT,
    visibility REAL CHECK (visibility >= 0 AND visibility <= 1),
    ambiguity REAL CHECK (ambiguity >= 0 AND ambiguity <= 1),
    systemic_connection REAL CHECK (systemic_connection >= 0 AND systemic_connection <= 1),
    propagation_potential REAL CHECK (propagation_potential >= 0 AND propagation_potential <= 1),
    institutional_recognition REAL CHECK (institutional_recognition >= 0 AND institutional_recognition <= 1),
    distributional_relevance REAL CHECK (distributional_relevance >= 0 AND distributional_relevance <= 1),
    monitoring_urgency REAL CHECK (monitoring_urgency >= 0 AND monitoring_urgency <= 1),
    affected_groups TEXT,
    description TEXT
);

CREATE TABLE early_indicators (
    indicator_id TEXT PRIMARY KEY,
    signal_id TEXT,
    indicator_name TEXT NOT NULL,
    evidence_count INTEGER,
    repetition_score REAL CHECK (repetition_score >= 0 AND repetition_score <= 1),
    clarity_score REAL CHECK (clarity_score >= 0 AND clarity_score <= 1),
    measurement_quality REAL CHECK (measurement_quality >= 0 AND measurement_quality <= 1),
    policy_attention REAL CHECK (policy_attention >= 0 AND policy_attention <= 1),
    indicator_status TEXT,
    review_frequency TEXT,
    FOREIGN KEY(signal_id) REFERENCES weak_signals(signal_id)
);

CREATE TABLE signal_clusters (
    cluster_id TEXT PRIMARY KEY,
    cluster_name TEXT NOT NULL,
    related_signals TEXT,
    domain TEXT,
    coherence REAL CHECK (coherence >= 0 AND coherence <= 1),
    strategic_concern REAL CHECK (strategic_concern >= 0 AND strategic_concern <= 1),
    monitoring_priority TEXT,
    description TEXT
);

CREATE TABLE propagation_pathways (
    pathway_id TEXT PRIMARY KEY,
    signal_id TEXT,
    pathway_type TEXT,
    adoption REAL CHECK (adoption >= 0 AND adoption <= 1),
    feedback REAL CHECK (feedback >= 0 AND feedback <= 1),
    institutional_recognition REAL CHECK (institutional_recognition >= 0 AND institutional_recognition <= 1),
    friction REAL CHECK (friction >= 0 AND friction <= 1),
    legitimacy REAL CHECK (legitimacy >= 0 AND legitimacy <= 1),
    scaling_condition TEXT,
    FOREIGN KEY(signal_id) REFERENCES weak_signals(signal_id)
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    domain TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    exposure REAL CHECK (exposure >= 0 AND exposure <= 1),
    reversibility REAL CHECK (reversibility >= 0 AND reversibility <= 1),
    monitoring_signal TEXT
);

CREATE TABLE watchlist (
    watch_id TEXT PRIMARY KEY,
    signal_id TEXT,
    watch_reason TEXT,
    owner_role TEXT,
    review_frequency TEXT,
    decision_linkage REAL CHECK (decision_linkage >= 0 AND decision_linkage <= 1),
    trigger_condition TEXT,
    FOREIGN KEY(signal_id) REFERENCES weak_signals(signal_id)
);

CREATE VIEW weak_signal_profiles AS
SELECT
    signal_id,
    signal_title,
    domain,
    signal_type,
    ROUND(
      0.10 * visibility -
      0.08 * ambiguity +
      0.24 * systemic_connection +
      0.22 * propagation_potential +
      0.12 * institutional_recognition +
      0.12 * distributional_relevance +
      0.20 * monitoring_urgency,
      4
    ) AS weak_signal_profile
FROM weak_signals;

CREATE VIEW early_indicator_scores AS
SELECT
    indicator_id,
    signal_id,
    indicator_name,
    ROUND(
      0.25 * repetition_score +
      0.25 * clarity_score +
      0.20 * measurement_quality +
      0.20 * policy_attention +
      0.10 * (evidence_count / 10.0),
      4
    ) AS early_indicator_score,
    indicator_status,
    review_frequency
FROM early_indicators;

CREATE VIEW signal_cluster_priorities AS
SELECT
    cluster_id,
    cluster_name,
    domain,
    ROUND(coherence * strategic_concern, 4) AS cluster_priority,
    monitoring_priority
FROM signal_clusters;

CREATE VIEW propagation_pathway_scores AS
SELECT
    pathway_id,
    signal_id,
    pathway_type,
    ROUND(
      0.25 * adoption +
      0.25 * feedback +
      0.20 * institutional_recognition +
      0.15 * legitimacy -
      0.20 * friction,
      4
    ) AS propagation_strength,
    scaling_condition
FROM propagation_pathways;

CREATE VIEW assumption_vulnerability_scores AS
SELECT
    assumption_id,
    domain,
    assumption_text,
    ROUND(exposure * (1 - confidence) * (1 + (1 - reversibility)), 4) AS vulnerability_score,
    monitoring_signal
FROM assumptions;
