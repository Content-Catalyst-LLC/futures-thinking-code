# Base R workflow for Scenario Modeling for Complex Systems.
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

scenarios <- read.csv(file.path(data_dir, "scenario_assumptions.csv"))
strategies <- read.csv(file.path(data_dir, "strategy_portfolio.csv"))
drivers <- read.csv(file.path(data_dir, "driver_register.csv"))

time_steps <- 1:40
rows <- list()
row_index <- 1

for (i in seq_len(nrow(scenarios))) {
  for (j in seq_len(nrow(strategies))) {
    scenario <- scenarios[i, ]
    strategy <- strategies[j, ]

    state <- 1.0 + strategy$baseline_boost
    capacity <- scenario$adaptation_gain + strategy$adaptation_boost

    governance_effect <- scenario$governance_capacity * strategy$governance_dependency * 0.015
    legitimacy_effect <- scenario$public_trust * 0.010
    equity_penalty <- max(0, scenario$distributional_pressure - strategy$equity_weight) * 0.035
    complexity_penalty <- strategy$implementation_complexity * 0.006

    for (t in time_steps) {
      if (t > 1) {
        periodic_shock <- ifelse(t %% 8 == 0, scenario$shock_level, scenario$shock_level / 3.0)
        absorbed_shock <- max(0, periodic_shock - strategy$shock_absorption)
        stress <- max(0, 1.0 - state)
        stress_feedback <- scenario$feedback_strength * stress

        capacity <- min(
          0.30,
          capacity +
            scenario$learning_gain * stress +
            0.002 * strategy$adaptation_boost +
            governance_effect
        )

        state <- state +
          scenario$growth_rate -
          absorbed_shock -
          stress_feedback +
          capacity +
          legitimacy_effect -
          equity_penalty -
          complexity_penalty

        state <- max(0, min(2, state))
      }

      rows[[row_index]] <- data.frame(
        scenario_id = scenario$scenario_id,
        scenario_name = scenario$scenario_name,
        strategy_id = strategy$strategy_id,
        strategy_name = strategy$strategy_name,
        time_step = t,
        system_state = round(state, 4),
        adaptive_capacity = round(capacity, 4)
      )
      row_index <- row_index + 1
    }
  }
}

paths <- do.call(rbind, rows)

summary_rows <- list()
summary_index <- 1

keys <- unique(paths[, c("scenario_id", "scenario_name", "strategy_id", "strategy_name")])

for (i in seq_len(nrow(keys))) {
  subset <- paths[
    paths$scenario_id == keys$scenario_id[i] &
    paths$strategy_id == keys$strategy_id[i],
  ]

  states <- subset$system_state
  capacities <- subset$adaptive_capacity

  final_state <- tail(states, 1)
  min_state <- min(states)
  mean_state <- mean(states)
  final_capacity <- tail(capacities, 1)

  viability <- 0.35 * final_state + 0.30 * min_state + 0.20 * mean_state + 0.15 * final_capacity

  summary_rows[[summary_index]] <- data.frame(
    scenario_id = keys$scenario_id[i],
    scenario_name = keys$scenario_name[i],
    strategy_id = keys$strategy_id[i],
    strategy_name = keys$strategy_name[i],
    final_state = round(final_state, 4),
    min_state = round(min_state, 4),
    mean_state = round(mean_state, 4),
    max_state = round(max(states), 4),
    final_adaptive_capacity = round(final_capacity, 4),
    viability_score = round(viability, 4)
  )
  summary_index <- summary_index + 1
}

summary <- do.call(rbind, summary_rows)

robustness_rows <- list()
robustness_index <- 1

for (strategy_id in unique(summary$strategy_id)) {
  subset <- summary[summary$strategy_id == strategy_id, ]
  robustness_rows[[robustness_index]] <- data.frame(
    strategy_id = strategy_id,
    strategy_name = subset$strategy_name[1],
    worst_case_viability = round(min(subset$viability_score), 4),
    mean_viability = round(mean(subset$viability_score), 4),
    best_case_viability = round(max(subset$viability_score), 4)
  )
  robustness_index <- robustness_index + 1
}

robustness <- do.call(rbind, robustness_rows)
robustness <- robustness[order(-robustness$worst_case_viability, -robustness$mean_viability), ]

drivers$driver_priority_score <- round(
  0.25 * drivers$impact_level +
  0.25 * drivers$uncertainty_level +
  0.20 * drivers$interaction_strength +
  0.15 * drivers$time_sensitivity +
  0.15 * drivers$monitoring_need,
  4
)
drivers <- drivers[order(-drivers$driver_priority_score), ]

write.csv(paths, file.path(outputs_dir, "r_scenario_strategy_paths.csv"), row.names = FALSE)
write.csv(summary, file.path(outputs_dir, "r_scenario_strategy_summary.csv"), row.names = FALSE)
write.csv(robustness, file.path(outputs_dir, "r_scenario_strategy_robustness.csv"), row.names = FALSE)
write.csv(drivers, file.path(outputs_dir, "r_driver_priority_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_strategy_robustness_scores.png"), width = 1200, height = 800)
barplot(
  robustness$worst_case_viability,
  names.arg = robustness$strategy_name,
  horiz = TRUE,
  las = 1,
  main = "Strategy Robustness Across Scenarios",
  xlab = "Worst-case viability"
)
dev.off()

print(robustness)
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
