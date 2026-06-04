# Base R workflow for Food, Water, and Land-Use Futures.
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

profiles <- read.csv(file.path(data_dir, "food_water_land_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "adaptation_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "resource_risk_indicators.csv"))

profiles$food_water_land_resilience_score <- round(
  0.13 * profiles$production_capacity +
  0.16 * profiles$water_security +
  0.15 * profiles$soil_health +
  0.14 * profiles$biodiversity_integrity +
  0.14 * profiles$governance_capacity -
  0.12 * profiles$climate_exposure -
  0.08 * profiles$market_vulnerability +
  0.14 * profiles$justice_capacity +
  0.12 * profiles$livelihood_resilience,
  4
)

profiles$food_water_land_fragility_score <- round(
  0.16 * profiles$climate_exposure +
  0.14 * profiles$market_vulnerability +
  0.14 * (1 - profiles$water_security) +
  0.13 * (1 - profiles$soil_health) +
  0.12 * (1 - profiles$biodiversity_integrity) +
  0.12 * (1 - profiles$governance_capacity) +
  0.10 * (1 - profiles$justice_capacity) +
  0.06 * (1 - profiles$livelihood_resilience) +
  0.03 * (1 - profiles$production_capacity),
  4
)

profiles <- profiles[order(-profiles$food_water_land_resilience_score), ]

strategies$resource_strategy_value_score <- round(
  0.12 * strategies$production_gain +
  0.16 * strategies$water_gain +
  0.16 * strategies$soil_gain +
  0.15 * strategies$biodiversity_gain +
  0.14 * strategies$governance_gain +
  0.15 * strategies$justice_gain +
  0.08 * strategies$livelihood_gain +
  0.04 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$resource_strategy_value_score), ]

risks$resource_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$cascade_potential +
  0.12 * risks$visibility_gap +
  0.14 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$resource_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_food_water_land_profile_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_adaptation_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_resource_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_food_water_land_resilience_scores.png"), width = 1200, height = 800)
barplot(
  profiles$food_water_land_resilience_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Food-Water-Land Resilience Scores",
  xlab = "Resilience score"
)
dev.off()

png(file.path(outputs_dir, "r_food_water_land_fragility_scores.png"), width = 1200, height = 800)
barplot(
  profiles$food_water_land_fragility_score,
  names.arg = profiles$future_name,
  horiz = TRUE,
  las = 1,
  main = "Food-Water-Land Fragility Scores",
  xlab = "Fragility score"
)
dev.off()

print(profiles[, c("profile_id", "future_name", "food_water_land_resilience_score", "food_water_land_fragility_score")])
print(strategies[, c("strategy_id", "strategy_name", "resource_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
