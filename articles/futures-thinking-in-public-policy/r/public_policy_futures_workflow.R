# Base R workflow for Futures Thinking in Public Policy.
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

policies <- read.csv(file.path(data_dir, "policy_options.csv"))
scenarios <- read.csv(file.path(data_dir, "scenario_profiles.csv"))
capacity <- read.csv(file.path(data_dir, "institutional_capacity.csv"))

policies$policy_futures_profile_score <- round(
  0.20 * policies$robustness +
  0.16 * policies$equity +
  0.18 * policies$adaptability +
  0.14 * policies$coordination +
  0.14 * policies$legitimacy +
  0.08 * policies$implementation_capacity +
  0.06 * policies$learning_capacity +
  0.04 * policies$intergenerational_responsibility,
  4
)

policies$policy_fragility_pressure_score <- round(
  0.20 * (1 - policies$robustness) +
  0.18 * (1 - policies$adaptability) +
  0.16 * (1 - policies$coordination) +
  0.14 * (1 - policies$legitimacy) +
  0.12 * (1 - policies$equity) +
  0.10 * (1 - policies$learning_capacity) +
  0.10 * (1 - policies$implementation_capacity),
  4
)

policies <- policies[order(-policies$policy_futures_profile_score), ]

scenarios$policy_stress_pressure_score <- round(
  0.18 * scenarios$economic_volatility +
  0.16 * scenarios$technological_disruption +
  0.18 * scenarios$climate_stress +
  0.12 * scenarios$demographic_pressure +
  0.16 * scenarios$geopolitical_instability +
  0.10 * (1 - scenarios$public_trust) +
  0.06 * (1 - scenarios$institutional_capacity) +
  0.04 * (1 - scenarios$fiscal_space),
  4
)

scenarios$governance_opportunity_score <- round(
  0.24 * scenarios$public_trust +
  0.24 * scenarios$institutional_capacity +
  0.18 * scenarios$fiscal_space +
  0.12 * (1 - scenarios$economic_volatility) +
  0.10 * (1 - scenarios$geopolitical_instability) +
  0.12 * (1 - scenarios$climate_stress),
  4
)

scenarios <- scenarios[order(-scenarios$policy_stress_pressure_score), ]

capacity$anticipatory_governance_capacity_score <- round(
  0.18 * capacity$detection_capacity +
  0.18 * capacity$learning_capacity +
  0.16 * capacity$coordination_quality +
  0.12 * capacity$budget_alignment +
  0.12 * capacity$implementation_capacity +
  0.10 * capacity$public_participation +
  0.08 * capacity$data_infrastructure +
  0.06 * capacity$accountability_capacity,
  4
)

capacity$capacity_gap_score <- round(1 - capacity$anticipatory_governance_capacity_score, 4)
capacity <- capacity[order(-capacity$anticipatory_governance_capacity_score), ]

write.csv(policies, file.path(outputs_dir, "r_policy_option_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_scenario_profile_scores.csv"), row.names = FALSE)
write.csv(capacity, file.path(outputs_dir, "r_institutional_capacity_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_policy_futures_profile_scores.png"), width = 1200, height = 800)
barplot(
  policies$policy_futures_profile_score,
  names.arg = policies$policy_name,
  horiz = TRUE,
  las = 1,
  main = "Policy Futures Profile Scores",
  xlab = "Policy futures profile"
)
dev.off()

png(file.path(outputs_dir, "r_policy_stress_pressure_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$policy_stress_pressure_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Policy Stress Pressure by Scenario",
  xlab = "Policy stress pressure"
)
dev.off()

print(policies[, c("policy_id", "policy_name", "policy_futures_profile_score", "policy_fragility_pressure_score")])
print(capacity[, c("capacity_id", "institution_name", "anticipatory_governance_capacity_score", "capacity_gap_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
