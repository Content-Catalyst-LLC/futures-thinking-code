-- Futures Wheel and Impact Mapping schema.
-- SQLite compatible.

DROP VIEW IF EXISTS distributional_risk_scores;
DROP VIEW IF EXISTS monitoring_gap_scores;
DROP VIEW IF EXISTS intervention_usefulness_scores;
DROP VIEW IF EXISTS impact_pathway_scores;
DROP VIEW IF EXISTS actor_leverage_scores;
DROP VIEW IF EXISTS edge_influence_scores;
DROP VIEW IF EXISTS consequence_priority_scores;

DROP TABLE IF EXISTS distributional_audit;
DROP TABLE IF EXISTS monitoring_indicators;
DROP TABLE IF EXISTS interventions;
DROP TABLE IF EXISTS impact_pathways;
DROP TABLE IF EXISTS actors;
DROP TABLE IF EXISTS consequence_edges;
DROP TABLE IF EXISTS consequence_nodes;
DROP TABLE IF EXISTS focal_changes;

CREATE TABLE focal_changes (
    focal_id TEXT PRIMARY KEY,
    focal_change TEXT NOT NULL,
    domain TEXT,
    time_horizon INTEGER,
    description TEXT
);

CREATE TABLE consequence_nodes (
    node_id TEXT PRIMARY KEY,
    focal_id TEXT,
    parent_node_id TEXT,
    consequence_order INTEGER,
    consequence TEXT NOT NULL,
    domain TEXT,
    likelihood REAL,
    severity REAL,
    uncertainty REAL,
    distributional_burden REAL,
    actionability REAL,
    affected_groups TEXT,
    description TEXT,
    FOREIGN KEY(focal_id) REFERENCES focal_changes(focal_id)
);

CREATE TABLE consequence_edges (
    edge_id TEXT PRIMARY KEY,
    source_node_id TEXT,
    target_node_id TEXT,
    relationship_type TEXT,
    influence_strength REAL,
    feedback_potential REAL,
    notes TEXT,
    FOREIGN KEY(source_node_id) REFERENCES consequence_nodes(node_id),
    FOREIGN KEY(target_node_id) REFERENCES consequence_nodes(node_id)
);

CREATE TABLE actors (
    actor_id TEXT PRIMARY KEY,
    actor_name TEXT NOT NULL,
    actor_type TEXT,
    domain TEXT,
    decision_power REAL,
    implementation_role REAL,
    affectedness REAL,
    knowledge_value REAL,
    description TEXT
);

CREATE TABLE impact_pathways (
    pathway_id TEXT PRIMARY KEY,
    focal_id TEXT,
    goal TEXT,
    actor_id TEXT,
    desired_impact TEXT,
    deliverable TEXT,
    indicator TEXT,
    traceability_score REAL,
    equity_relevance REAL,
    implementation_feasibility REAL,
    FOREIGN KEY(focal_id) REFERENCES focal_changes(focal_id),
    FOREIGN KEY(actor_id) REFERENCES actors(actor_id)
);

CREATE TABLE interventions (
    intervention_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    intervention_type TEXT,
    intervention_name TEXT,
    cost_complexity REAL,
    time_to_impact REAL,
    institutional_dependency REAL,
    risk_reduction REAL,
    notes TEXT,
    FOREIGN KEY(pathway_id) REFERENCES impact_pathways(pathway_id)
);

CREATE TABLE monitoring_indicators (
    indicator_id TEXT PRIMARY KEY,
    pathway_id TEXT,
    indicator_name TEXT,
    baseline REAL,
    target REAL,
    review_frequency TEXT,
    decision_trigger TEXT,
    FOREIGN KEY(pathway_id) REFERENCES impact_pathways(pathway_id)
);

CREATE TABLE distributional_audit (
    audit_id TEXT PRIMARY KEY,
    node_id TEXT,
    affected_group TEXT,
    exposure REAL,
    adaptive_capacity REAL,
    decision_voice REAL,
    burden_shift_risk REAL,
    priority_note TEXT,
    FOREIGN KEY(node_id) REFERENCES consequence_nodes(node_id)
);

CREATE VIEW consequence_priority_scores AS
SELECT
    node_id,
    focal_id,
    parent_node_id,
    consequence_order,
    consequence,
    domain,
    ROUND(
      0.22 * likelihood +
      0.26 * severity +
      0.14 * uncertainty +
      0.22 * distributional_burden +
      0.16 * actionability,
      4
    ) AS priority_score,
    affected_groups
FROM consequence_nodes;

CREATE VIEW edge_influence_scores AS
SELECT
    edge_id,
    source_node_id,
    target_node_id,
    relationship_type,
    ROUND(influence_strength * (1 + feedback_potential), 4) AS edge_priority
FROM consequence_edges;

CREATE VIEW actor_leverage_scores AS
SELECT
    actor_id,
    actor_name,
    actor_type,
    domain,
    ROUND(
      0.30 * decision_power +
      0.25 * implementation_role +
      0.20 * affectedness +
      0.25 * knowledge_value,
      4
    ) AS actor_leverage_score
FROM actors;

CREATE VIEW impact_pathway_scores AS
SELECT
    pathway_id,
    focal_id,
    actor_id,
    goal,
    desired_impact,
    deliverable,
    indicator,
    ROUND(
      0.40 * traceability_score +
      0.30 * equity_relevance +
      0.30 * implementation_feasibility,
      4
    ) AS impact_pathway_score
FROM impact_pathways;

CREATE VIEW intervention_usefulness_scores AS
SELECT
    intervention_id,
    pathway_id,
    intervention_type,
    intervention_name,
    ROUND(
      0.40 * risk_reduction +
      0.25 * time_to_impact +
      0.20 * (1 - cost_complexity) +
      0.15 * (1 - institutional_dependency),
      4
    ) AS intervention_usefulness_score
FROM interventions;

CREATE VIEW monitoring_gap_scores AS
SELECT
    indicator_id,
    pathway_id,
    indicator_name,
    baseline,
    target,
    ROUND(ABS(target - baseline), 4) AS monitoring_gap,
    review_frequency,
    decision_trigger
FROM monitoring_indicators;

CREATE VIEW distributional_risk_scores AS
SELECT
    audit_id,
    node_id,
    affected_group,
    ROUND(
      0.35 * exposure +
      0.30 * (1 - adaptive_capacity) +
      0.20 * (1 - decision_voice) +
      0.15 * burden_shift_risk,
      4
    ) AS distributional_risk_score,
    priority_note
FROM distributional_audit;
