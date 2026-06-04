# Base R workflow for Planetary Boundaries and Future Pathways.
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

profiles <- read.csv(file.path(data_dir, "planetary_pathway_profiles.csv"))
strategies <- read.csv(file.path(data_dir, "pathway_strategy_options.csv"))
risks <- read.csv(file.path(data_dir, "planetary_risk_indicators.csv"))

profiles$total_boundary_pressure_score <- round(
  0.16 * profiles$climate_pressure +
  0.16 * profiles$biosphere_pressure +
  0.12 * profiles$land_pressure +
  0.12 * profiles$freshwater_pressure +
  0.10 * profiles$nutrient_pressure +
  0.10 * profiles$ocean_pressure +
  0.08 * profiles$aerosol_pressure +
  0.10 * profiles$novel_entity_pressure +
  0.06 * profiles$technology_dependence,
  4
)

profiles$safe_and_just_pathway_score <- round(
  0.22 * profiles$social_foundation_security +
  0.20 * profiles$governance_capacity +
  0.20 * profiles$justice_capacity +
  0.14 * profiles$regeneration_capacity -
  0.20 * profiles$total_boundary_pressure_score +
  0.04 * (1 - profiles$technology_dependence),
  4
)

profiles <- profiles[order(-profiles$safe_and_just_pathway_score), ]

strategies$pathway_strategy_value_score <- round(
  0.14 * strategies$climate_reduction +
  0.14 * strategies$biosphere_recovery +
  0.11 * strategies$land_restoration +
  0.11 * strategies$water_security +
  0.09 * strategies$nutrient_circularity +
  0.09 * strategies$novel_entity_control +
  0.12 * strategies$social_foundation_gain +
  0.10 * strategies$governance_gain +
  0.08 * strategies$justice_gain +
  0.02 * strategies$implementation_capacity,
  4
)

strategies <- strategies[order(-strategies$pathway_strategy_value_score), ]

risks$planetary_risk_priority_score <- round(
  0.14 * risks$probability_proxy +
  0.18 * risks$severity +
  0.17 * risks$cascade_potential +
  0.12 * risks$visibility_gap +
  0.14 * risks$recovery_difficulty +
  0.17 * risks$distributional_harm +
  0.08 * (1 - risks$preparedness),
  4
)

risks <- risks[order(-risks$planetary_risk_priority_score), ]

write.csv(profiles, file.path(outputs_dir, "r_planetary_pathway_scores.csv"), row.names = FALSE)
write.csv(strategies, file.path(outputs_dir, "r_pathway_strategy_scores.csv"), row.names = FALSE)
write.csv(risks, file.path(outputs_dir, "r_planetary_risk_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_safe_and_just_pathway_scores.png"), width = 1200, height = 800)
barplot(
  profiles$safe_and_just_pathway_score,
  names.arg = profiles$pathway_name,
  horiz = TRUE,
  las = 1,
  main = "Safe-and-Just Pathway Scores",
  xlab = "Pathway score"
)
dev.off()

png(file.path(outputs_dir, "r_boundary_pressure_scores.png"), width = 1200, height = 800)
barplot(
  profiles$total_boundary_pressure_score,
  names.arg = profiles$pathway_name,
  horiz = TRUE,
  las = 1,
  main = "Total Boundary Pressure Scores",
  xlab = "Boundary pressure"
)
dev.off()

print(profiles[, c("pathway_id", "pathway_name", "total_boundary_pressure_score", "safe_and_just_pathway_score")])
print(strategies[, c("strategy_id", "strategy_name", "pathway_strategy_value_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
