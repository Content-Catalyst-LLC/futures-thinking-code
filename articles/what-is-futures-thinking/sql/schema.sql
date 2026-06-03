-- Research-grade Futures Thinking schema scaffold.
-- SQLite compatible.

DROP TABLE IF EXISTS strategy_evaluations;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS signals;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS forecast_observations;
DROP TABLE IF EXISTS practice_profiles;

CREATE TABLE drivers (
    driver_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    uncertainty REAL NOT NULL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL NOT NULL CHECK (impact >= 0 AND impact <= 1),
    velocity REAL NOT NULL CHECK (velocity >= 0 AND velocity <= 1),
    description TEXT
);

CREATE TABLE signals (
    signal_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    signal TEXT NOT NULL,
    uncertainty REAL NOT NULL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL NOT NULL CHECK (impact >= 0 AND impact <= 1),
    novelty REAL NOT NULL CHECK (novelty >= 0 AND novelty <= 1),
    source_type TEXT,
    monitoring_priority TEXT
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    summary TEXT,
    plausibility REAL CHECK (plausibility >= 0 AND plausibility <= 1),
    time_horizon_years INTEGER,
    system_stress REAL CHECK (system_stress >= 0 AND system_stress <= 1)
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
    strategy_name TEXT NOT NULL,
    strategy_type TEXT,
    description TEXT,
    adaptability REAL CHECK (adaptability >= 0 AND adaptability <= 1),
    implementation_difficulty REAL CHECK (implementation_difficulty >= 0 AND implementation_difficulty <= 1),
    equity_sensitivity REAL CHECK (equity_sensitivity >= 0 AND equity_sensitivity <= 1)
);

CREATE TABLE strategy_evaluations (
    evaluation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_id TEXT NOT NULL,
    scenario_id TEXT NOT NULL,
    performance REAL NOT NULL CHECK (performance >= 0 AND performance <= 1),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    notes TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY(scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE forecast_observations (
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric TEXT NOT NULL,
    period TEXT NOT NULL,
    observed_value REAL NOT NULL,
    forecast_value REAL NOT NULL,
    domain TEXT,
    forecast_error REAL GENERATED ALWAYS AS (observed_value - forecast_value) VIRTUAL,
    absolute_error REAL GENERATED ALWAYS AS (ABS(observed_value - forecast_value)) VIRTUAL
);

CREATE TABLE practice_profiles (
    practice TEXT PRIMARY KEY,
    predictive_emphasis REAL,
    uncertainty_plurality REAL,
    assumption_visibility REAL,
    participatory_depth REAL,
    strategic_readiness REAL,
    critical_reflection REAL,
    reproducibility REAL
);

CREATE VIEW signal_watch_scores AS
SELECT
    signal_id,
    domain,
    signal,
    ROUND(0.35 * uncertainty + 0.40 * impact + 0.25 * novelty, 4) AS watch_score,
    monitoring_priority
FROM signals;

CREATE VIEW driver_priority_scores AS
SELECT
    driver_id,
    domain,
    driver_name,
    ROUND(uncertainty * impact * velocity, 4) AS driver_priority
FROM drivers;

CREATE VIEW assumption_vulnerability_scores AS
SELECT
    assumption_id,
    domain,
    assumption_text,
    ROUND(exposure * (1 - confidence) * (1 + (1 - reversibility)), 4) AS vulnerability_score,
    monitoring_signal
FROM assumptions;
