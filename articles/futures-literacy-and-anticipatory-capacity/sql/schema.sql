-- Futures Literacy and Anticipatory Capacity schema.
-- SQLite compatible.

DROP TABLE IF EXISTS strategy_translation;
DROP TABLE IF EXISTS learning_cycles;
DROP TABLE IF EXISTS future_images;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS capacity_profiles;

CREATE TABLE capacity_profiles (
    organization_type TEXT PRIMARY KEY,
    scanning_capacity REAL CHECK (scanning_capacity >= 0 AND scanning_capacity <= 1),
    interpretive_capacity REAL CHECK (interpretive_capacity >= 0 AND interpretive_capacity <= 1),
    assumption_visibility REAL CHECK (assumption_visibility >= 0 AND assumption_visibility <= 1),
    imagination_range REAL CHECK (imagination_range >= 0 AND imagination_range <= 1),
    participatory_depth REAL CHECK (participatory_depth >= 0 AND participatory_depth <= 1),
    learning_capacity REAL CHECK (learning_capacity >= 0 AND learning_capacity <= 1),
    action_translation REAL CHECK (action_translation >= 0 AND action_translation <= 1)
);

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    domain TEXT NOT NULL,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    exposure REAL CHECK (exposure >= 0 AND exposure <= 1),
    reversibility REAL CHECK (reversibility >= 0 AND reversibility <= 1),
    monitoring_signal TEXT
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    signal TEXT NOT NULL,
    uncertainty REAL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL CHECK (impact >= 0 AND impact <= 1),
    novelty REAL CHECK (novelty >= 0 AND novelty <= 1),
    source_type TEXT,
    monitoring_priority TEXT
);

CREATE TABLE future_images (
    future_image_id TEXT PRIMARY KEY,
    actor_group TEXT NOT NULL,
    future_image TEXT NOT NULL,
    dominant_emotion TEXT,
    time_horizon INTEGER,
    assumption_risk REAL CHECK (assumption_risk >= 0 AND assumption_risk <= 1),
    participation_need REAL CHECK (participation_need >= 0 AND participation_need <= 1)
);

CREATE TABLE learning_cycles (
    cycle_id TEXT PRIMARY KEY,
    cycle_name TEXT NOT NULL,
    signal_review_frequency TEXT,
    assumption_review_frequency TEXT,
    public_participation_level REAL,
    decision_linkage REAL,
    learning_score REAL
);

CREATE TABLE strategy_translation (
    insight_id TEXT PRIMARY KEY,
    insight TEXT NOT NULL,
    decision_area TEXT,
    action_option TEXT,
    monitoring_indicator TEXT,
    review_frequency TEXT
);

CREATE VIEW assumption_vulnerability_scores AS
SELECT
    assumption_id,
    domain,
    assumption_text,
    ROUND(exposure * (1 - confidence) * (1 + (1 - reversibility)), 4) AS vulnerability_score,
    monitoring_signal
FROM assumptions;

CREATE VIEW signal_watch_scores AS
SELECT
    signal_id,
    domain,
    signal,
    ROUND(0.35 * uncertainty + 0.40 * impact + 0.25 * novelty, 4) AS watch_score,
    monitoring_priority
FROM signals;
