-- Trend Analysis and Megatrends schema.
-- SQLite compatible.

DROP TABLE IF EXISTS strategy_implications;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS megatrend_interactions;
DROP TABLE IF EXISTS trend_profiles;

CREATE TABLE trend_profiles (
    trend_id TEXT PRIMARY KEY,
    pattern_type TEXT NOT NULL,
    domain TEXT,
    pattern_class TEXT,
    momentum REAL CHECK (momentum >= 0 AND momentum <= 1),
    structural_depth REAL CHECK (structural_depth >= 0 AND structural_depth <= 1),
    cross_system_influence REAL CHECK (cross_system_influence >= 0 AND cross_system_influence <= 1),
    reversibility REAL CHECK (reversibility >= 0 AND reversibility <= 1),
    uncertainty REAL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    distributional_sensitivity REAL CHECK (distributional_sensitivity >= 0 AND distributional_sensitivity <= 1),
    description TEXT
);

CREATE TABLE megatrend_interactions (
    interaction_id TEXT PRIMARY KEY,
    source_trend TEXT NOT NULL,
    target_trend TEXT NOT NULL,
    interaction_type TEXT,
    interaction_strength REAL CHECK (interaction_strength >= 0 AND interaction_strength <= 1),
    systemic_risk REAL CHECK (systemic_risk >= 0 AND systemic_risk <= 1),
    description TEXT,
    FOREIGN KEY(source_trend) REFERENCES trend_profiles(trend_id),
    FOREIGN KEY(target_trend) REFERENCES trend_profiles(trend_id)
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    domain TEXT,
    signal TEXT NOT NULL,
    related_trend TEXT,
    uncertainty REAL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL CHECK (impact >= 0 AND impact <= 1),
    novelty REAL CHECK (novelty >= 0 AND novelty <= 1),
    source_type TEXT,
    monitoring_priority TEXT,
    FOREIGN KEY(related_trend) REFERENCES trend_profiles(trend_id)
);

CREATE TABLE indicators (
    indicator_id TEXT PRIMARY KEY,
    indicator_name TEXT NOT NULL,
    domain TEXT,
    trend_id TEXT,
    current_value REAL,
    baseline_value REAL,
    trend_direction TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    review_frequency TEXT,
    FOREIGN KEY(trend_id) REFERENCES trend_profiles(trend_id)
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

CREATE TABLE strategy_implications (
    implication_id TEXT PRIMARY KEY,
    trend_id TEXT,
    strategic_implication TEXT NOT NULL,
    decision_area TEXT,
    action_option TEXT,
    monitoring_indicator TEXT,
    review_frequency TEXT,
    decision_linkage REAL CHECK (decision_linkage >= 0 AND decision_linkage <= 1),
    FOREIGN KEY(trend_id) REFERENCES trend_profiles(trend_id)
);

CREATE VIEW trend_megatrend_profile_scores AS
SELECT
    trend_id,
    pattern_type,
    domain,
    ROUND(
      0.20 * momentum +
      0.22 * structural_depth +
      0.22 * cross_system_influence -
      0.12 * reversibility -
      0.14 * uncertainty +
      0.10 * distributional_sensitivity,
      4
    ) AS long_term_change_profile
FROM trend_profiles;

CREATE VIEW megatrend_interaction_priorities AS
SELECT
    interaction_id,
    source_trend,
    target_trend,
    interaction_type,
    ROUND(interaction_strength * systemic_risk, 4) AS interaction_priority
FROM megatrend_interactions;

CREATE VIEW signal_watch_scores AS
SELECT
    signal_id,
    domain,
    related_trend,
    signal,
    ROUND(0.35 * uncertainty + 0.40 * impact + 0.25 * novelty, 4) AS watch_score,
    monitoring_priority
FROM signals;

CREATE VIEW assumption_vulnerability_scores AS
SELECT
    assumption_id,
    domain,
    assumption_text,
    ROUND(exposure * (1 - confidence) * (1 + (1 - reversibility)), 4) AS vulnerability_score,
    monitoring_signal
FROM assumptions;
