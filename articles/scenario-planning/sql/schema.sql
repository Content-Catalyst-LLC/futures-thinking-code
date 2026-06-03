-- Scenario Planning schema.
-- SQLite compatible.

DROP TABLE IF EXISTS strategy_performance;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS drivers_uncertainties;
DROP TABLE IF EXISTS scenario_framework;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    archetype TEXT,
    summary TEXT,
    plausibility REAL CHECK (plausibility >= 0 AND plausibility <= 1),
    system_stress REAL CHECK (system_stress >= 0 AND system_stress <= 1),
    time_horizon_years INTEGER
);

CREATE TABLE scenario_framework (
    axis_id TEXT PRIMARY KEY,
    axis_name TEXT NOT NULL,
    low_end TEXT,
    high_end TEXT,
    why_it_matters TEXT
);

CREATE TABLE drivers_uncertainties (
    driver_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    driver_or_uncertainty TEXT NOT NULL,
    driver_type TEXT CHECK (driver_type IN ('driver', 'critical_uncertainty')),
    uncertainty REAL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL CHECK (impact >= 0 AND impact <= 1),
    velocity REAL CHECK (velocity >= 0 AND velocity <= 1),
    description TEXT
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

CREATE TABLE assumptions (
    assumption_id TEXT PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    domain TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    exposure REAL CHECK (exposure >= 0 AND exposure <= 1),
    reversibility REAL CHECK (reversibility >= 0 AND reversibility <= 1),
    monitoring_signal TEXT
);

CREATE TABLE strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy TEXT NOT NULL,
    strategy_type TEXT,
    description TEXT,
    adaptability REAL CHECK (adaptability >= 0 AND adaptability <= 1),
    equity_sensitivity REAL CHECK (equity_sensitivity >= 0 AND equity_sensitivity <= 1),
    implementation_difficulty REAL CHECK (implementation_difficulty >= 0 AND implementation_difficulty <= 1)
);

CREATE TABLE strategy_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    performance REAL CHECK (performance >= 0 AND performance <= 1),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    notes TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY(scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE VIEW driver_criticality_scores AS
SELECT
    driver_id,
    domain,
    driver_or_uncertainty,
    driver_type,
    ROUND(uncertainty * impact * velocity, 4) AS criticality_score
FROM drivers_uncertainties;

CREATE VIEW signal_watch_scores AS
SELECT
    signal_id,
    domain,
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
