# Base R workflow for Societal Transformation and Long-Term Change.
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

drivers <- read.csv(file.path(data_dir, "transformation_drivers.csv"))
scenarios <- read.csv(file.path(data_dir, "transformation_scenarios.csv"))
equity <- read.csv(file.path(data_dir, "equity_indicators.csv"))

drivers$driver_transformation_priority <- round(
  0.18 * drivers$transformative_intensity +
  0.14 * drivers$uncertainty +
  0.16 * drivers$system_reach +
  0.14 * drivers$feedback_strength +
  0.14 * drivers$threshold_proximity +
  0.12 * drivers$governance_relevance +
  0.12 * drivers$equity_relevance,
  4
)

drivers <- drivers[order(-drivers$driver_transformation_priority), ]

scenarios$transformation_depth_score <- round(
  0.18 * scenarios$technology_intensity +
  0.18 * scenarios$economic_restructuring +
  0.18 * scenarios$ecological_stress +
  0.16 * scenarios$institutional_adaptability +
  0.14 * scenarios$social_cohesion +
  0.08 * scenarios$equity_protection +
  0.08 * scenarios$public_legitimacy,
  4
)

scenarios$just_transformation_capacity_score <- round(
  0.22 * scenarios$institutional_adaptability +
  0.22 * scenarios$equity_protection +
  0.20 * scenarios$public_legitimacy +
  0.18 * scenarios$social_cohesion +
  0.10 * (1 - scenarios$ecological_stress) +
  0.08 * scenarios$economic_restructuring,
  4
)

scenarios$fragility_score <- round(
  0.26 * scenarios$ecological_stress +
  0.22 * (1 - scenarios$institutional_adaptability) +
  0.20 * (1 - scenarios$social_cohesion) +
  0.18 * (1 - scenarios$public_legitimacy) +
  0.14 * (1 - scenarios$equity_protection),
  4
)

scenarios$transformation_class <- ifelse(
  scenarios$just_transformation_capacity_score >= 0.72,
  "Strong just-transformation capacity",
  ifelse(scenarios$fragility_score >= 0.62, "Fragile or high-risk transformation", "Contested transition pathway")
)

scenarios <- scenarios[order(-scenarios$just_transformation_capacity_score), ]

equity$justice_capacity_score <- round(
  0.20 * equity$voice +
  0.22 * equity$protection +
  0.22 * equity$repair +
  0.18 * equity$agency +
  0.18 * (1 - equity$burden_concentration),
  4
)

equity$harm_concentration_score <- round(
  0.30 * equity$exposure +
  0.30 * equity$burden_concentration +
  0.16 * (1 - equity$voice) +
  0.12 * (1 - equity$protection) +
  0.12 * (1 - equity$agency),
  4
)

equity <- equity[order(-equity$justice_capacity_score), ]

write.csv(drivers, file.path(outputs_dir, "r_transformation_driver_scores.csv"), row.names = FALSE)
write.csv(scenarios, file.path(outputs_dir, "r_transformation_scenario_scores.csv"), row.names = FALSE)
write.csv(equity, file.path(outputs_dir, "r_equity_justice_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_transformation_scenario_scores.png"), width = 1200, height = 800)
barplot(
  scenarios$just_transformation_capacity_score,
  names.arg = scenarios$scenario_name,
  horiz = TRUE,
  las = 1,
  main = "Just Transformation Capacity Scores",
  xlab = "Just transformation capacity"
)
dev.off()

png(file.path(outputs_dir, "r_driver_transformation_priority.png"), width = 1200, height = 800)
barplot(
  drivers$driver_transformation_priority,
  names.arg = drivers$driver_name,
  horiz = TRUE,
  las = 1,
  main = "Transformation Driver Priority Scores",
  xlab = "Driver priority"
)
dev.off()

print(scenarios[, c("scenario_id", "scenario_name", "just_transformation_capacity_score", "fragility_score", "transformation_class")])
print(drivers[, c("driver_id", "driver_name", "driver_transformation_priority")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
