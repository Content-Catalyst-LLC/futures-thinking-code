# Base R workflow for Digital Platform Futures.
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

platforms <- read.csv(file.path(data_dir, "platform_profiles.csv"))
scenarios <- read.csv(file.path(data_dir, "platform_scenarios.csv"))
accountability <- read.csv(file.path(data_dir, "accountability_indicators.csv"))

platforms$platform_power_score <- round(
  0.26 * platforms$network_effect_strength +
  0.24 * platforms$data_advantage +
  0.22 * platforms$gatekeeping_power +
  0.16 * platforms$lock_in +
  0.12 * (1 - platforms$interoperability),
  4
)

platforms$public_interest_platform_capacity_score <- round(
  0.18 * platforms$interoperability +
  0.18 * platforms$public_accountability +
  0.16 * platforms$user_rights +
  0.14 * platforms$worker_protection +
  0.14 * platforms$digital_public_value +
  0.10 * platforms$ecological_responsibility +
  0.05 * (1 - platforms$platform_power_score) +
  0.05 * (1 - platforms$data_advantage),
  4
)

platforms$platform_dependency_pressure_score <- round(
  0.24 * platforms$platform_power_score +
  0.20 * platforms$data_advantage +
  0.18 * (1 - platforms$interoperability) +
  0.14 * (1 - platforms$user_rights) +
  0.14 * (1 - platforms$public_accountability) +
  0.10 * (1 - platforms$worker_protection),
  4
)

platforms <- platforms[order(-platforms$platform_dependency_pressure_score), ]

scenarios$public_interest_platform_capacity_score <- round(
  0.18 * scenarios$interoperability +
  0.18 * scenarios$public_accountability +
  0.16 * scenarios$user_rights +
  0.14 * scenarios$worker_protection +
  0.14 * scenarios$digital_public_value +
  0.10 * scenarios$ecological_responsibility +
  0.05 * (1 - scenarios$platform_power) +
  0.05 * (1 - scenarios$data_advantage),
  4
)

scenarios$platform_dependency_pressure_score <- round(
  0.24 * scenarios$platform_power +
  0.20 * scenarios$data_advantage +
  0.18 * (1 - scenarios$interoperability) +
  0.14 * (1 - scenarios$user_rights) +
  0.14 * (1 - scenarios$public_accountability) +
  0.10 * (1 - scenarios$worker_protection),
  4
)

scenarios <- scenarios[order(-scenarios$public_interest_platform_capacity_score), ]

accountability$accountability_capacity_score <- round(
  0.18 * accountability$transparency +
  0.16 * accountability$auditability +
  0.18 * accountability$contestability +
  0.18 * accountability$enforceability +
  0.10 * accountability$researcher_access +
  0.12 * accountability$remedy_capacity +
  0.08 * accountability$public_participation,
  4
)

accountability$accountability_gap_score <- round(1 - accountability$accountability_capacity_score, 4)
accountability <- accountability[order(-accountability$accountability_gap_score), ]

write.csv(platforms, file.path(outputs_dir, "r_platform_profile_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_platform_scenario_scores.csv"), row.names = FALSE)
write.csv(accountability, file.path(outputs_dir, "r_platform_accountability_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_platform_dependency_pressure_scores.png"), width = 1200, height = 800)
barplot(
  platforms$platform_dependency_pressure_score,
  names.arg = platforms$platform_name,
  horiz = TRUE,
  las = 1,
  main = "Platform Dependency Pressure Scores",
  xlab = "Platform dependency pressure"
)
dev.off()

png(file.path(outputs_dir, "r_public_interest_platform_capacity_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$public_interest_platform_capacity_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Public-Interest Platform Capacity by Scenario",
  xlab = "Public-interest platform capacity"
)
dev.off()

print(platforms[, c("platform_id", "platform_name", "platform_power_score", "platform_dependency_pressure_score", "public_interest_platform_capacity_score")])
print(scenarios[, c("scenario_id", "scenario_name", "public_interest_platform_capacity_score", "platform_dependency_pressure_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
