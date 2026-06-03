# Base R workflow for Systems Foresight and Structural Change.
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

systems <- read.csv(file.path(data_dir, "system_domains.csv"))
leverage <- read.csv(file.path(data_dir, "leverage_points.csv"))
strategies <- read.csv(file.path(data_dir, "strategy_pathways.csv"))

systems$structural_pressure_score <- round(
  0.22 * systems$system_stress +
  0.16 * (1 - systems$adaptive_capacity) +
  0.14 * (1 - systems$public_trust) +
  0.16 * systems$interdependence +
  0.14 * systems$distributional_vulnerability +
  0.09 * systems$institutional_fragmentation +
  0.09 * systems$structural_lock_in,
  4
)

systems$pressure_class <- ifelse(
  systems$structural_pressure_score >= 0.78,
  "High structural pressure",
  ifelse(
    systems$structural_pressure_score >= 0.68,
    "Significant structural pressure",
    "Moderate structural pressure"
  )
)

systems <- systems[order(-systems$structural_pressure_score), ]

leverage$leverage_score <- round(
  leverage$intervention_depth *
  leverage$system_reach *
  leverage$political_feasibility *
  leverage$legitimacy_quality *
  leverage$equity_quality *
  leverage$implementation_readiness,
  4
)

leverage <- leverage[order(-leverage$leverage_score), ]

structural_pressure <- function(stress, capacity, trust, interdependence, vulnerability) {
  0.26 * stress +
    0.22 * (1 - capacity) +
    0.18 * (1 - trust) +
    0.18 * interdependence +
    0.16 * vulnerability
}

paths <- list()
path_index <- 1

for (i in seq_len(nrow(strategies))) {
  strategy <- strategies[i, ]
  stress <- 0.84
  capacity <- 0.42
  trust <- 0.46
  interdependence <- 0.86
  vulnerability <- 0.88

  for (t in 1:40) {
    shock <- ifelse(t %% 10 == 0, 0.08, 0.02)
    learning_effect <- strategy$structural_depth * max(0, 0.75 - capacity) * 0.010
    implementation_drag <- strategy$implementation_complexity * 0.002
    coordination_bonus <- strategy$governance_dependency * strategy$structural_depth * 0.0015

    stress <- min(1, max(0, stress + shock - strategy$stress_reduction - learning_effect - coordination_bonus))
    capacity <- min(1, max(0, capacity + strategy$capacity_gain + learning_effect - implementation_drag))
    trust <- min(1, max(0, trust + strategy$trust_gain - 0.020 * shock + 0.003 * strategy$structural_depth))
    vulnerability <- min(1, max(0, vulnerability - strategy$vulnerability_reduction + 0.010 * shock - 0.002 * strategy$structural_depth))

    pressure <- structural_pressure(stress, capacity, trust, interdependence, vulnerability)

    paths[[path_index]] <- data.frame(
      strategy_id = strategy$strategy_id,
      strategy_name = strategy$strategy_name,
      strategy_type = strategy$strategy_type,
      time_step = t,
      stress = round(stress, 4),
      adaptive_capacity = round(capacity, 4),
      trust = round(trust, 4),
      interdependence = round(interdependence, 4),
      distributional_vulnerability = round(vulnerability, 4),
      structural_pressure = round(pressure, 4)
    )
    path_index <- path_index + 1
  }
}

pathways <- do.call(rbind, paths)

summary_rows <- list()
summary_index <- 1

for (strategy_id in unique(pathways$strategy_id)) {
  subset <- pathways[pathways$strategy_id == strategy_id, ]
  final <- subset[nrow(subset), ]

  change_score <- 0.30 * (1 - final$structural_pressure) +
    0.25 * final$adaptive_capacity +
    0.20 * final$trust +
    0.25 * (1 - final$distributional_vulnerability)

  summary_rows[[summary_index]] <- data.frame(
    strategy_id = strategy_id,
    strategy_name = final$strategy_name,
    strategy_type = final$strategy_type,
    final_pressure = final$structural_pressure,
    mean_pressure = round(mean(subset$structural_pressure), 4),
    max_pressure = round(max(subset$structural_pressure), 4),
    final_capacity = final$adaptive_capacity,
    final_trust = final$trust,
    final_vulnerability = final$distributional_vulnerability,
    structural_change_score = round(change_score, 4)
  )
  summary_index <- summary_index + 1
}

summary <- do.call(rbind, summary_rows)
summary <- summary[order(-summary$structural_change_score), ]

write.csv(systems, file.path(outputs_dir, "r_structural_pressure_scores.csv"), row.names = FALSE)
write.csv(leverage, file.path(outputs_dir, "r_leverage_point_scores.csv"), row.names = FALSE)
write.csv(pathways, file.path(outputs_dir, "r_structural_change_pathways.csv"), row.names = FALSE)
write.csv(summary, file.path(outputs_dir, "r_structural_change_summary.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_structural_pressure_scores.png"), width = 1200, height = 800)
barplot(
  systems$structural_pressure_score,
  names.arg = systems$system_domain,
  horiz = TRUE,
  las = 1,
  main = "Structural Pressure by System Domain",
  xlab = "Structural pressure score"
)
dev.off()

print(systems[, c("system_domain", "structural_pressure_score", "pressure_class")])
print(summary[, c("strategy_name", "final_pressure", "structural_change_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
