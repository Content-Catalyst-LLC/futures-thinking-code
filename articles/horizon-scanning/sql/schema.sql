-- Horizon Scanning schema.
-- SQLite compatible.

DROP TABLE IF EXISTS institutional_profiles;
DROP TABLE IF EXISTS watchlist;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS signal_clusters;
DROP TABLE IF EXISTS sources;
DROP TABLE IF EXISTS signals;

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    signal_title TEXT NOT NULL,
    domain TEXT,
    signal_type TEXT,
    visibility REAL CHECK (visibility >= 0 AND visibility <= 1),
    ambiguity REAL CHECK (ambiguity >= 0 AND ambiguity <= 1),
    structural_connection REAL CHECK (structural_connection >= 0 AND structural_connection <= 1),
    domain_diversity REAL CHECK (domain_diversity >= 0 AND domain_diversity <= 1),
    source_diversity REAL CHECK (source_diversity >= 0 AND source_diversity <= 1),
    assumption_challenge REAL CHECK (assumption_challenge >= 0 AND assumption_challenge <= 1),
    strategic_relevance REAL CHECK (strategic_relevance >= 0 AND strategic_relevance <= 1),
    affected_groups TEXT,
    description TEXT
);

CREATE TABLE sources (
    source_id TEXT PRIMARY KEY,
    source_name TEXT NOT NULL,
    source_type TEXT,
    domain TEXT,
    elite_source TEXT,
    community_source TEXT,
    scientific_source TEXT,
    policy_source TEXT,
    cultural_source TEXT,
    reliability REAL CHECK (reliability >= 0 AND reliability <= 1),
    blind_spot_risk REAL CHECK (blind_spot_risk >= 0 AND blind_spot_risk <= 1),
    description TEXT
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
    FOREIGN KEY(signal_id) REFERENCES signals(signal_id)
);

CREATE TABLE institutional_profiles (
    profile_id TEXT PRIMARY KEY,
    profile_name TEXT NOT NULL,
    signal_strength REAL CHECK (signal_strength >= 0 AND signal_strength <= 1),
    ambiguity REAL CHECK (ambiguity >= 0 AND ambiguity <= 1),
    filtering_quality REAL CHECK (filtering_quality >= 0 AND filtering_quality <= 1),
    source_diversity REAL CHECK (source_diversity >= 0 AND source_diversity <= 1),
    institutional_uptake REAL CHECK (institutional_uptake >= 0 AND institutional_uptake <= 1),
    resistance REAL CHECK (resistance >= 0 AND resistance <= 1)
);

CREATE VIEW horizon_signal_profiles AS
SELECT
    signal_id,
    signal_title,
    domain,
    signal_type,
    ROUND(
      0.10 * visibility -
      0.08 * ambiguity +
      0.22 * structural_connection +
      0.18 * domain_diversity +
      0.14 * source_diversity +
      0.14 * assumption_challenge +
      0.30 * strategic_relevance,
      4
    ) AS horizon_scanning_profile
FROM signals;

CREATE VIEW signal_cluster_priorities AS
SELECT
    cluster_id,
    cluster_name,
    domain,
    ROUND(coherence * strategic_concern, 4) AS cluster_priority,
    monitoring_priority
FROM signal_clusters;

CREATE VIEW assumption_vulnerability_scores AS
SELECT
    assumption_id,
    domain,
    assumption_text,
    ROUND(exposure * (1 - confidence) * (1 + (1 - reversibility)), 4) AS vulnerability_score,
    monitoring_signal
FROM assumptions;

CREATE VIEW institutional_scanning_effectiveness AS
SELECT
    profile_id,
    profile_name,
    ROUND(
      0.20 * signal_strength -
      0.16 * ambiguity +
      0.24 * filtering_quality +
      0.22 * source_diversity +
      0.22 * institutional_uptake -
      0.16 * resistance,
      4
    ) AS scanning_effectiveness_score
FROM institutional_profiles;
