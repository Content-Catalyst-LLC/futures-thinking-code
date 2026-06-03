-- Strategic Robustness Across Futures schema.
-- SQLite compatible.

DROP VIEW IF EXISTS assumption_fragility_scores;
DROP VIEW IF EXISTS vulnerability_priority_scores;
DROP VIEW IF EXISTS adaptive_trigger_scores;
DROP VIEW IF EXISTS strategy_regret_summary;
DROP VIEW IF EXISTS scenario_strategy_regret;
DROP VIEW IF EXISTS strategy_robustness_scores;
DROP VIEW IF EXISTS scenario_strategy_performance;

DROP TABLE IF EXISTS assumption_register;
DROP TABLE IF EXISTS vulnerability_conditions;
DROP TABLE IF EXISTS adaptive_triggers;
DROP TABLE IF EXISTS performance_criteria;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    scenario_family TEXT,
    disruption_level REAL,
    public_trust REAL,
    fiscal_capacity REAL,
    implementation_capacity REAL,
    ecological_stress REAL,
    technology_volatility REAL,
    distributional_pressure REAL,
    description TEXT
);

CREATE TABLE strategies (
    strategy_id TEXT PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    strategy_type TEXT,
    baseline_effectiveness REAL,
    shock_absorption REAL,
    equity_quality REAL,
    adaptability REAL,
    implementation_complexity REAL,
    legitimacy_design REAL,
    transformability REAL,
    description TEXT
);

CREATE TABLE performance_criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT,
    weight REAL,
    description TEXT
);

CREATE TABLE adaptive_triggers (
    trigger_id TEXT PRIMARY KEY,
    indicator_name TEXT,
    baseline REAL,
    threshold_value REAL,
    review_frequency TEXT,
    linked_scenario TEXT,
    trigger_rule TEXT,
    decision_response TEXT
);

CREATE TABLE vulnerability_conditions (
    vulnerability_id TEXT PRIMARY KEY,
    strategy_id TEXT,
    scenario_id TEXT,
    vulnerability_name TEXT,
    severity REAL,
    detectability REAL,
    mitigation_capacity REAL,
    description TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY(scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE assumption_register (
    assumption_id TEXT PRIMARY KEY,
    strategy_id TEXT,
    assumption_name TEXT,
    assumption_text TEXT,
    confidence REAL,
    fragility REAL,
    monitoring_indicator TEXT,
    revision_rule TEXT,
    FOREIGN KEY(strategy_id) REFERENCES strategies(strategy_id)
);

CREATE VIEW scenario_strategy_performance AS
SELECT
    s.scenario_id,
    s.scenario_name,
    st.strategy_id,
    st.strategy_name,
    ROUND(
      MAX(0, MIN(1,
        st.baseline_effectiveness -
        0.22 * s.disruption_level +
        0.26 * st.shock_absorption -
        0.08 * s.ecological_stress -
        0.05 * s.technology_volatility * (1 - st.adaptability)
      )),
      4
    ) AS effectiveness,
    ROUND(
      MAX(0, MIN(1,
        s.implementation_capacity +
        0.18 * s.fiscal_capacity -
        0.30 * st.implementation_complexity -
        0.05 * s.disruption_level
      )),
      4
    ) AS feasibility,
    ROUND(
      MAX(0, MIN(1,
        0.40 * s.public_trust +
        0.25 * st.legitimacy_design +
        0.20 * st.equity_quality +
        0.15 * st.adaptability -
        0.05 * s.distributional_pressure
      )),
      4
    ) AS legitimacy,
    ROUND(
      MAX(0, MIN(1,
        st.equity_quality -
        0.30 * s.distributional_pressure +
        0.15 * st.legitimacy_design +
        0.10 * st.transformability
      )),
      4
    ) AS equity,
    ROUND(
      MAX(0, MIN(1,
        0.70 * st.adaptability +
        0.30 * s.implementation_capacity -
        0.05 * s.technology_volatility * (1 - st.shock_absorption)
      )),
      4
    ) AS adaptability_score,
    ROUND(
      MAX(0, MIN(1,
        0.70 * st.transformability +
        0.30 * st.legitimacy_design -
        0.06 * st.implementation_complexity
      )),
      4
    ) AS transformability_score,
    ROUND(
      MAX(0, MIN(1,
        0.24 * MAX(0, MIN(1, st.baseline_effectiveness - 0.22 * s.disruption_level + 0.26 * st.shock_absorption - 0.08 * s.ecological_stress - 0.05 * s.technology_volatility * (1 - st.adaptability))) +
        0.18 * MAX(0, MIN(1, s.implementation_capacity + 0.18 * s.fiscal_capacity - 0.30 * st.implementation_complexity - 0.05 * s.disruption_level)) +
        0.18 * MAX(0, MIN(1, 0.40 * s.public_trust + 0.25 * st.legitimacy_design + 0.20 * st.equity_quality + 0.15 * st.adaptability - 0.05 * s.distributional_pressure)) +
        0.16 * MAX(0, MIN(1, st.equity_quality - 0.30 * s.distributional_pressure + 0.15 * st.legitimacy_design + 0.10 * st.transformability)) +
        0.14 * MAX(0, MIN(1, 0.70 * st.adaptability + 0.30 * s.implementation_capacity - 0.05 * s.technology_volatility * (1 - st.shock_absorption))) +
        0.10 * MAX(0, MIN(1, 0.70 * st.transformability + 0.30 * st.legitimacy_design - 0.06 * st.implementation_complexity))
      )),
      4
    ) AS viability_score
FROM scenarios s
CROSS JOIN strategies st;

CREATE VIEW strategy_robustness_scores AS
SELECT
    strategy_id,
    strategy_name,
    ROUND(MIN(viability_score), 4) AS worst_case_viability,
    ROUND(AVG(viability_score), 4) AS mean_viability,
    ROUND(MAX(viability_score), 4) AS best_case_viability,
    ROUND(MAX(viability_score) - MIN(viability_score), 4) AS viability_range,
    SUM(CASE WHEN viability_score < 0.50 THEN 1 ELSE 0 END) AS threshold_failures
FROM scenario_strategy_performance
GROUP BY strategy_id, strategy_name;

CREATE VIEW scenario_strategy_regret AS
SELECT
    p.scenario_id,
    p.scenario_name,
    p.strategy_id,
    p.strategy_name,
    p.viability_score,
    ROUND(b.best_scenario_viability, 4) AS best_scenario_viability,
    ROUND(b.best_scenario_viability - p.viability_score, 4) AS regret
FROM scenario_strategy_performance p
JOIN (
    SELECT scenario_id, MAX(viability_score) AS best_scenario_viability
    FROM scenario_strategy_performance
    GROUP BY scenario_id
) b ON p.scenario_id = b.scenario_id;

CREATE VIEW strategy_regret_summary AS
SELECT
    strategy_id,
    strategy_name,
    ROUND(MAX(regret), 4) AS max_regret,
    ROUND(AVG(regret), 4) AS mean_regret
FROM scenario_strategy_regret
GROUP BY strategy_id, strategy_name;

CREATE VIEW adaptive_trigger_scores AS
SELECT
    trigger_id,
    indicator_name,
    baseline,
    threshold_value,
    ROUND(ABS(threshold_value - baseline), 4) AS monitoring_gap,
    review_frequency,
    linked_scenario,
    ROUND(
      0.45 * ABS(threshold_value - baseline) +
      0.35 * threshold_value +
      0.20 *
        CASE review_frequency
          WHEN 'monthly' THEN 1.00
          WHEN 'quarterly' THEN 0.88
          WHEN 'semiannual' THEN 0.68
          WHEN 'annual' THEN 0.48
          ELSE 0.50
        END,
      4
    ) AS trigger_priority_score,
    trigger_rule,
    decision_response
FROM adaptive_triggers;

CREATE VIEW vulnerability_priority_scores AS
SELECT
    vulnerability_id,
    strategy_id,
    scenario_id,
    vulnerability_name,
    ROUND(
      0.50 * severity +
      0.25 * (1 - detectability) +
      0.25 * (1 - mitigation_capacity),
      4
    ) AS vulnerability_priority_score,
    description
FROM vulnerability_conditions;

CREATE VIEW assumption_fragility_scores AS
SELECT
    assumption_id,
    strategy_id,
    assumption_name,
    ROUND(0.45 * (1 - confidence) + 0.55 * fragility, 4) AS assumption_failure_risk,
    monitoring_indicator,
    revision_rule
FROM assumption_register;
