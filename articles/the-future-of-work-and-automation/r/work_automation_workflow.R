# Base R workflow for The Future of Work and Automation.
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

occupations <- read.csv(file.path(data_dir, "occupation_profiles.csv"))
scenarios <- read.csv(file.path(data_dir, "work_scenarios.csv"))
protections <- read.csv(file.path(data_dir, "social_protection_indicators.csv"))

occupations$exposure_pressure_score <- round(
  0.34 * occupations$task_exposure +
  0.22 * occupations$surveillance_intensity +
  0.18 * (1 - occupations$worker_voice) +
  0.14 * (1 - occupations$training_access) +
  0.12 * (1 - occupations$social_protection),
  4
)

occupations$worker_centered_capacity_score <- round(
  0.20 * occupations$augmentation_capacity +
  0.20 * occupations$worker_voice +
  0.16 * occupations$training_access +
  0.16 * occupations$social_protection +
  0.14 * occupations$wage_security +
  0.14 * (1 - occupations$surveillance_intensity),
  4
)

occupations$transition_risk_score <- round(
  occupations$task_exposure *
  (1 - occupations$training_access) *
  (1 - occupations$social_protection + occupations$surveillance_intensity / 2),
  4
)

occupations <- occupations[order(-occupations$transition_risk_score), ]

scenarios$worker_centered_capacity_score <- round(
  0.18 * scenarios$augmentation_capacity +
  0.18 * scenarios$worker_voice +
  0.18 * scenarios$job_quality +
  0.14 * scenarios$transition_support +
  0.14 * scenarios$skill_mobility +
  0.12 * scenarios$social_protection +
  0.06 * (1 - scenarios$surveillance_intensity),
  4
)

scenarios$displacement_control_pressure_score <- round(
  0.30 * scenarios$automation_intensity +
  0.22 * scenarios$surveillance_intensity +
  0.18 * (1 - scenarios$transition_support) +
  0.16 * (1 - scenarios$skill_mobility) +
  0.14 * (1 - scenarios$social_protection),
  4
)

scenarios <- scenarios[order(-scenarios$worker_centered_capacity_score), ]

protections$social_protection_readiness_score <- round(
  0.16 * protections$training_access +
  0.16 * protections$income_support +
  0.14 * protections$portable_benefits +
  0.14 * protections$wage_floor +
  0.14 * protections$appeal_rights +
  0.14 * protections$collective_bargaining_access +
  0.12 * protections$public_investment,
  4
)

protections$social_protection_gap_score <- round(1 - protections$social_protection_readiness_score, 4)
protections <- protections[order(-protections$social_protection_gap_score), ]

write.csv(occupations, file.path(outputs_dir, "r_occupation_future_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_work_scenario_scores.csv"), row.names = FALSE)
write.csv(protections, file.path(outputs_dir, "r_social_protection_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_occupation_transition_risk_scores.png"), width = 1200, height = 800)
barplot(
  occupations$transition_risk_score,
  names.arg = occupations$occupation_name,
  horiz = TRUE,
  las = 1,
  main = "Occupation Transition Risk Scores",
  xlab = "Transition risk"
)
dev.off()

png(file.path(outputs_dir, "r_worker_centered_scenario_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$worker_centered_capacity_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Worker-Centered Scenario Scores",
  xlab = "Worker-centered capacity"
)
dev.off()

print(occupations[, c("occupation_id", "occupation_name", "transition_risk_score", "worker_centered_capacity_score")])
print(scenarios[, c("scenario_id", "scenario_name", "worker_centered_capacity_score", "displacement_control_pressure_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
