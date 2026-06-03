# Base R workflow for Supply Chain Futures.
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

profiles <- read.csv(file.path(data_dir, "supply_chain_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "resilience_strategies.csv"))
chokepoints <- read.csv(file.path(data_dir, "chokepoint_risk_register.csv"))

profiles$supply_chain_resilience_score <- round(
  0.10 * profiles$cost_efficiency +
  0.16 * profiles$supplier_diversification +
  0.14 * profiles$inventory_buffer +
  0.14 * profiles$supply_visibility +
  0.12 * profiles$labor_accountability +
  0.13 * profiles$climate_adaptation +
  0.09 * profiles$digital_traceability +
  0.06 * profiles$circularity +
  0.04 * profiles$regulatory_readiness +
  0.02 * profiles$recovery_capacity,
  4
)

profiles$supply_chain_fragility_score <- round(
  0.16 * (1 - profiles$supplier_diversification) +
  0.16 * (1 - profiles$inventory_buffer) +
  0.14 * (1 - profiles$supply_visibility) +
  0.14 * (1 - profiles$climate_adaptation) +
  0.12 * (1 - profiles$labor_accountability) +
  0.10 * (1 - profiles$recovery_capacity) +
  0.08 * (1 - profiles$regulatory_readiness) +
  0.06 * (1 - profiles$digital_traceability) +
  0.04 * (1 - profiles$circularity),
  4
)

profiles <- profiles[order(-profiles$supply_chain_resilience_score), ]

strategies$resilience_gain_score <- round(
  0.18 * strategies$supplier_diversification_gain +
  0.16 * strategies$buffer_gain +
  0.16 * strategies$visibility_gain +
  0.14 * strategies$labor_accountability_gain +
  0.16 * strategies$climate_adaptation_gain +
  0.10 * strategies$circularity_gain +
  0.10 * strategies$implementation_capacity -
  0.10 * strategies$cost_burden,
  4
)

strategies <- strategies[order(-strategies$resilience_gain_score), ]

chokepoints$chokepoint_priority_score <- round(
  0.18 * chokepoints$dependency_concentration +
  0.17 * chokepoints$substitution_difficulty +
  0.16 * chokepoints$disruption_probability +
  0.18 * chokepoints$systemic_reach +
  0.17 * chokepoints$recovery_difficulty +
  0.14 * chokepoints$visibility_gap,
  4
)

chokepoints <- chokepoints[order(-chokepoints$chokepoint_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_supply_chain_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_resilience_strategy_scores.csv"), row.names = FALSE)
write.csv(chokepoints, file.path(outputs_dir, "r_chokepoint_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_supply_chain_resilience_scores.png"), width = 1200, height = 800)
barplot(
  profiles$supply_chain_resilience_score,
  names.arg = profiles$supply_chain_name,
  horiz = TRUE,
  las = 1,
  main = "Supply Chain Resilience Scores",
  xlab = "Resilience score"
)
dev.off()

png(file.path(outputs_dir, "r_supply_chain_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$supply_chain_fragility_score,
  names.arg = profiles$supply_chain_name,
  horiz = TRUE,
  las = 1,
  main = "Supply Chain Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "supply_chain_name", "supply_chain_resilience_score", "supply_chain_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "resilience_gain_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
