-- Possible, Plausible, Probable, and Preferable Futures schema.
-- SQLite compatible.

DROP TABLE IF EXISTS strategy_fit;
DROP TABLE IF EXISTS category_shifts;
DROP TABLE IF EXISTS preference_criteria;
DROP TABLE IF EXISTS candidate_futures;
DROP TABLE IF EXISTS drivers;

CREATE TABLE candidate_futures (
    future_id TEXT PRIMARY KEY,
    future TEXT NOT NULL,
    driver_support REAL CHECK (driver_support >= 0 AND driver_support <= 1),
    pathway_coherence REAL CHECK (pathway_coherence >= 0 AND pathway_coherence <= 1),
    constraint_fit REAL CHECK (constraint_fit >= 0 AND constraint_fit <= 1),
    current_trend_strength REAL CHECK (current_trend_strength >= 0 AND current_trend_strength <= 1),
    justice_value REAL CHECK (justice_value >= 0 AND justice_value <= 1),
    sustainability_value REAL CHECK (sustainability_value >= 0 AND sustainability_value <= 1),
    resilience_value REAL CHECK (resilience_value >= 0 AND resilience_value <= 1),
    legitimacy_value REAL CHECK (legitimacy_value >= 0 AND legitimacy_value <= 1),
    participation_need REAL CHECK (participation_need >= 0 AND participation_need <= 1)
);

CREATE TABLE preference_criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion TEXT NOT NULL,
    weight REAL CHECK (weight >= 0 AND weight <= 1),
    description TEXT
);

CREATE TABLE strategy_fit (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    probable_fit REAL,
    plausible_fit REAL,
    preferable_fit REAL,
    adaptive_capacity REAL,
    implementation_difficulty REAL,
    equity_sensitivity REAL
);

CREATE TABLE category_shifts (
    shift_id TEXT PRIMARY KEY,
    future_id TEXT NOT NULL,
    previous_category TEXT,
    current_category TEXT,
    signal TEXT,
    shift_strength REAL,
    monitoring_priority TEXT,
    FOREIGN KEY(future_id) REFERENCES candidate_futures(future_id)
);

CREATE TABLE drivers (
    driver_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    driver TEXT NOT NULL,
    uncertainty REAL,
    impact REAL,
    velocity REAL
);

CREATE VIEW future_category_scores AS
SELECT
    future_id,
    future,
    ROUND(0.40 * driver_support + 0.35 * pathway_coherence + 0.25 * constraint_fit, 4) AS plausibility_score,
    ROUND(0.70 * current_trend_strength + 0.30 * driver_support, 4) AS probability_score,
    ROUND(0.30 * justice_value + 0.25 * sustainability_value + 0.25 * resilience_value + 0.20 * legitimacy_value, 4) AS preference_score
FROM candidate_futures;

CREATE VIEW strategy_category_fit_scores AS
SELECT
    strategy_id,
    strategy,
    ROUND(
        0.20 * probable_fit +
        0.30 * plausible_fit +
        0.30 * preferable_fit +
        0.20 * adaptive_capacity -
        0.05 * implementation_difficulty +
        0.05 * equity_sensitivity,
        4
    ) AS category_fit_score
FROM strategy_fit;
