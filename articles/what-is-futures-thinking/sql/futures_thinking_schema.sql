-- Futures Thinking SQL schema
-- Educational schema for drivers, uncertainties, signals, scenarios, strategies, and evaluations.

CREATE TABLE IF NOT EXISTS futures_projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    description TEXT NOT NULL,
    time_horizon TEXT NOT NULL,
    boundary_note TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    driver_name TEXT NOT NULL,
    driver_domain TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES futures_projects(project_id)
);

CREATE TABLE IF NOT EXISTS uncertainties (
    uncertainty_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    uncertainty_name TEXT NOT NULL,
    uncertainty_level REAL NOT NULL,
    impact_level REAL NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES futures_projects(project_id)
);

CREATE TABLE IF NOT EXISTS weak_signals (
    signal_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    signal_domain TEXT NOT NULL,
    signal_description TEXT NOT NULL,
    novelty REAL NOT NULL,
    uncertainty REAL NOT NULL,
    potential_impact REAL NOT NULL,
    monitoring_priority REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES futures_projects(project_id)
);

CREATE TABLE IF NOT EXISTS scenarios (
    scenario_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    scenario_name TEXT NOT NULL,
    scenario_logic TEXT NOT NULL,
    assumptions TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES futures_projects(project_id)
);

CREATE TABLE IF NOT EXISTS strategies (
    strategy_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL,
    strategy_name TEXT NOT NULL,
    description TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES futures_projects(project_id)
);

CREATE TABLE IF NOT EXISTS strategy_evaluations (
    evaluation_id INTEGER PRIMARY KEY,
    strategy_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    performance_score REAL NOT NULL,
    interpretation_note TEXT,
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

INSERT INTO futures_projects
(project_id, project_name, description, time_horizon, boundary_note)
VALUES
(1, 'Strategic Readiness Across Multiple Futures', 'Synthetic foresight project for educational modeling.', '2030-2050', 'Boundary includes technology, climate, institutions, geopolitics, and sustainability transition.');

INSERT INTO drivers
(driver_id, project_id, driver_name, driver_domain, description)
VALUES
(1, 1, 'Artificial Intelligence Diffusion', 'Technology', 'Pace and governance of AI adoption.'),
(2, 1, 'Climate Stress', 'Environment', 'Intensity of climate impacts and adaptation pressure.'),
(3, 1, 'Institutional Trust', 'Governance', 'Public confidence in institutional competence and legitimacy.'),
(4, 1, 'Geopolitical Fragmentation', 'Global Order', 'Degree of international coordination or conflict.');
