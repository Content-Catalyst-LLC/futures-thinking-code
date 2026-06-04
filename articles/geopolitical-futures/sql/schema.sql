DROP VIEW IF EXISTS geopolitical_profile_scores;
DROP TABLE IF EXISTS geopolitical_futures_profiles;

CREATE TABLE geopolitical_futures_profiles (
    profile_id TEXT PRIMARY KEY,
    future_name TEXT NOT NULL,
    power_concentration REAL,
    interdependence REAL,
    institutional_coordination REAL,
    technological_competition REAL,
    climate_stress REAL,
    economic_vulnerability REAL,
    domestic_resilience REAL,
    information_integrity REAL,
    resource_security REAL,
    crisis_communication REAL,
    description TEXT
);

CREATE VIEW geopolitical_profile_scores AS
SELECT
    profile_id,
    future_name,
    ROUND(
      0.11 * (1 - power_concentration) +
      0.10 * interdependence +
      0.16 * institutional_coordination -
      0.12 * technological_competition -
      0.12 * climate_stress -
      0.11 * economic_vulnerability +
      0.12 * domestic_resilience +
      0.11 * information_integrity +
      0.08 * resource_security +
      0.07 * crisis_communication,
      4
    ) AS geopolitical_stability_score
FROM geopolitical_futures_profiles;
