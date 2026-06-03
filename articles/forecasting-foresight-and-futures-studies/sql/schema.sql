-- Forecasting, Foresight, and Futures Studies
-- SQLite-compatible schema for forecasts, drivers, scenarios, assumptions, strategies, and evaluations.

DROP TABLE IF EXISTS forecast_observations;
DROP TABLE IF EXISTS drivers;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS strategy_evaluations;

CREATE TABLE forecast_observations (
    observation_id INTEGER PRIMARY KEY,
    metric TEXT NOT NULL,
    period TEXT NOT NULL,
    observed_value REAL NOT NULL,
    forecast_value REAL NOT NULL,
    forecast_error REAL GENERATED ALWAYS AS (observed_value - forecast_value) VIRTUAL
);

CREATE TABLE drivers (
    driver_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    uncertainty REAL NOT NULL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL NOT NULL CHECK (impact >= 0 AND impact <= 1)
);

CREATE TABLE scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    narrative TEXT NOT NULL,
    plausibility_score REAL CHECK (plausibility_score >= 0 AND plausibility_score <= 1)
);

CREATE TABLE assumptions (
    assumption_id INTEGER PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    related_domain TEXT NOT NULL,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    vulnerability_note TEXT
);

CREATE TABLE strategies (
    strategy_id INTEGER PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT NOT NULL
);

CREATE TABLE strategy_evaluations (
    evaluation_id INTEGER PRIMARY KEY,
    strategy_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    performance REAL NOT NULL CHECK (performance >= 0 AND performance <= 1),
    notes TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY(scenario_id) REFERENCES scenarios(scenario_id)
);

INSERT INTO strategies(strategy_id, strategy_name, strategy_type) VALUES
(1, 'Forecast-Optimized Strategy', 'forecasting'),
(2, 'Flexible Foresight Strategy', 'foresight'),
(3, 'Transformational Strategy', 'futures_studies'),
(4, 'Defensive Continuity Strategy', 'risk_control');

INSERT INTO scenarios(scenario_id, scenario_name, narrative, plausibility_score) VALUES
(1, 'Expected Continuity', 'Baseline continuation of current assumptions.', 0.75),
(2, 'Technology Disruption', 'Rapid technological change destabilizes existing plans.', 0.72),
(3, 'Climate Stress', 'Climate impacts intensify across infrastructure and public systems.', 0.80),
(4, 'Institutional Fragmentation', 'Trust and institutional capacity weaken under compounded stress.', 0.68);
