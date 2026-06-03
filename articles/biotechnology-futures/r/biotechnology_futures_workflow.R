# Base R workflow for Biotechnology Futures.
# No external packages required.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("--file=", "", file_arg))
  root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  root <- normalizePath(".", mustWork = TRUE)
}

data_dir <- file.path(root, "data")
outputs_dir <- file.path(root, "outputs")
dir.create(outputs_dir, showWarnings = FALSE, recursive = TRUE)

capabilities <- read.csv(file.path(data_dir, "biotechnology_capabilities.csv"))
scenarios <- read.csv(file.path(data_dir, "biotechnology_scenarios.csv"))
justice <- read.csv(file.path(data_dir, "justice_indicators.csv"))

capacity_score <- function(science, governance, legitimacy, equity, manufacturing, consent, ecological_uncertainty, dual_use_risk) {
  0.16 * science +
    0.18 * governance +
    0.16 * legitimacy +
    0.16 * equity +
    0.12 * manufacturing +
    0.12 * consent +
    0.05 * (1 - ecological_uncertainty) +
    0.05 * (1 - dual_use_risk)
}

risk_pressure <- function(dual_use_risk, ecological_uncertainty, governance, legitimacy, consent, equity) {
  0.22 * dual_use_risk +
    0.20 * ecological_uncertainty +
    0.18 * (1 - governance) +
    0.16 * (1 - legitimacy) +
    0.14 * (1 - consent) +
    0.10 * (1 - equity)
}

capabilities$responsible_biotechnology_capacity_score <- round(
  capacity_score(
    capabilities$scientific_maturity,
    capabilities$governance_readiness,
    capabilities$public_legitimacy,
    capabilities$equity_access,
    capabilities$manufacturing_capacity,
    capabilities$community_consent,
    capabilities$ecological_uncertainty,
    capabilities$dual_use_risk
  ),
  4
)

capabilities$biological_risk_pressure_score <- round(
  risk_pressure(
    capabilities$dual_use_risk,
    capabilities$ecological_uncertainty,
    capabilities$governance_readiness,
    capabilities$public_legitimacy,
    capabilities$community_consent,
    capabilities$equity_access
  ),
  4
)

capabilities <- capabilities[order(-capabilities$responsible_biotechnology_capacity_score), ]

scenarios$responsible_biotechnology_capacity_score <- round(
  capacity_score(
    scenarios$scientific_maturity,
    scenarios$governance_readiness,
    scenarios$public_legitimacy,
    scenarios$equity_access,
    scenarios$manufacturing_capacity,
    scenarios$community_consent,
    scenarios$ecological_uncertainty,
    scenarios$dual_use_risk
  ),
  4
)

scenarios$biological_risk_pressure_score <- round(
  risk_pressure(
    scenarios$dual_use_risk,
    scenarios$ecological_uncertainty,
    scenarios$governance_readiness,
    scenarios$public_legitimacy,
    scenarios$community_consent,
    scenarios$equity_access
  ),
  4
)

scenarios$justice_profile_score <- round(
  0.28 * scenarios$equity_access +
  0.24 * scenarios$community_consent +
  0.20 * scenarios$public_legitimacy +
  0.16 * scenarios$governance_readiness +
  0.12 * (1 - scenarios$biological_risk_pressure_score),
  4
)

scenarios <- scenarios[order(-scenarios$responsible_biotechnology_capacity_score), ]

justice$biotechnology_justice_score <- round(
  0.20 * justice$equitable_access +
  0.16 * justice$affected_voice +
  0.16 * justice$consent_strength +
  0.16 * justice$benefit_sharing +
  0.14 * justice$repair_capacity +
  0.10 * justice$community_governance +
  0.08 * (1 - justice$harm_concentration),
  4
)

justice$harm_concentration_score <- round(
  0.32 * justice$harm_concentration +
  0.18 * (1 - justice$equitable_access) +
  0.16 * (1 - justice$affected_voice) +
  0.14 * (1 - justice$consent_strength) +
  0.12 * (1 - justice$repair_capacity) +
  0.08 * (1 - justice$community_governance),
  4
)

justice <- justice[order(-justice$biotechnology_justice_score), ]

write.csv(capabilities, file.path(outputs_dir, "r_biotechnology_capability_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_biotechnology_scenario_scores.csv"), row.names = FALSE)
write.csv(justice, file.path(outputs_dir, "r_biotechnology_justice_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_responsible_biotechnology_capacity_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$responsible_biotechnology_capacity_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Responsible Biotechnology Capacity by Scenario",
  xlab = "Responsible biotechnology capacity"
)
dev.off()

print(scenarios[, c("scenario_id", "scenario_name", "responsible_biotechnology_capacity_score", "biological_risk_pressure_score", "justice_profile_score")])
print(capabilities[, c("capability_id", "capability_name", "responsible_biotechnology_capacity_score", "biological_risk_pressure_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
