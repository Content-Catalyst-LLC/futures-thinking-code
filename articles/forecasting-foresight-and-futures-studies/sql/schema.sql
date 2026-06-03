-- Futures Thinking article schema scaffold.

CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    driver_name TEXT NOT NULL,
    uncertainty REAL CHECK (uncertainty >= 0 AND uncertainty <= 1),
    impact REAL CHECK (impact >= 0 AND impact <= 1)
);

CREATE TABLE IF NOT EXISTS signals (
    signal_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    signal_text TEXT NOT NULL,
    monitoring_priority TEXT
);

CREATE TABLE IF NOT EXISTS scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    narrative TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS assumptions (
    assumption_id INTEGER PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    vulnerability_note TEXT
);

CREATE TABLE IF NOT EXISTS strategy_evaluations (
    evaluation_id INTEGER PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    performance REAL CHECK (performance >= 0 AND performance <= 1)
);
