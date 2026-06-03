# Base R workflow for Institutional Adaptation.
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

profiles <- read.csv(file.path(data_dir, "institutional_profiles.csv"))
scenarios <- read.csv(file.path(data_dir, "adaptation_scenarios.csv"))
feedback <- read.csv(file.path(data_dir, "feedback_indicators.csv"))

profiles$adaptive_profile_score <- round(
  0.18 * profiles$learning_capacity +
  0.16 * profiles$structural_flexibility +
  0.16 * profiles$coordination_capacity +
  0.14 * profiles$legitimacy +
  0.14 * profiles$feedback_sensitivity +
  0.10 * profiles$resource_mobility +
  0.08 * profiles$shock_responsiveness -
  0.10 * profiles$rigidity +
  0.04 * profiles$intergenerational_responsibility,
  4
)

profiles$fragility_pressure_score <- round(
  0.20 * profiles$rigidity +
  0.16 * (1 - profiles$learning_capacity) +
  0.16 * (1 - profiles$structural_flexibility) +
  0.14 * (1 - profiles$coordination_capacity) +
  0.12 * (1 - profiles$legitimacy) +
  0.12 * (1 - profiles$feedback_sensitivity) +
  0.10 * (1 - profiles$resource_mobility),
  4
)

profiles <- profiles[order(-profiles$adaptive_profile_score), ]

scenarios$institutional_stress_pressure_score <- round(
  0.18 * scenarios$environmental_pressure +
  0.18 * scenarios$technological_change +
  0.14 * scenarios$demographic_pressure +
  0.14 * scenarios$fiscal_constraint +
  0.12 * (1 - scenarios$public_trust) +
  0.12 * scenarios$coordination_demand +
  0.12 * scenarios$crisis_frequency,
  4
)

scenarios$adaptation_opportunity_score <- round(
  0.24 * scenarios$public_trust +
  0.22 * (1 - scenarios$fiscal_constraint) +
  0.18 * (1 - scenarios$crisis_frequency) +
  0.14 * (1 - scenarios$environmental_pressure) +
  0.12 * (1 - scenarios$technological_change) +
  0.10 * scenarios$coordination_demand,
  4
)

scenarios <- scenarios[order(-scenarios$institutional_stress_pressure_score), ]

feedback$feedback_capacity_score <- round(
  0.18 * feedback$signal_detection +
  0.16 * feedback$interpretation_capacity +
  0.16 * feedback$evaluation_quality +
  0.14 * feedback$memory_retention +
  0.14 * feedback$revision_authority +
  0.12 * feedback$community_feedback +
  0.10 * feedback$public_reporting,
  4
)

feedback$feedback_gap_score <- round(1 - feedback$feedback_capacity_score, 4)
feedback <- feedback[order(-feedback$feedback_capacity_score), ]

write.csv(profiles, file.path(outputs_dir, "r_institutional_profile_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_adaptation_scenario_scores.csv"), row.names = FALSE)
write.csv(feedback, file.path(outputs_dir, "r_feedback_capacity_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_institutional_adaptive_profile_scores.png"), width = 1200, height = 800)
barplot(
  profiles$adaptive_profile_score,
  names.arg = profiles$institution_name,
  horiz = TRUE,
  las = 1,
  main = "Institutional Adaptive Profile Scores",
  xlab = "Adaptive profile"
)
dev.off()

png(file.path(outputs_dir, "r_institutional_stress_pressure_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$institutional_stress_pressure_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Institutional Stress Pressure by Scenario",
  xlab = "Institutional stress pressure"
)
dev.off()

print(profiles[, c("institution_id", "institution_name", "adaptive_profile_score", "fragility_pressure_score")])
print(scenarios[, c("scenario_id", "scenario_name", "institutional_stress_pressure_score", "adaptation_opportunity_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
