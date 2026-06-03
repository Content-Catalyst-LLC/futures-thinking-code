# Base R workflow for Strategic Robustness Across Futures.
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

scenarios <- read.csv(file.path(data_dir, "scenarios.csv"))
strategies <- read.csv(file.path(data_dir, "strategies.csv"))
criteria <- read.csv(file.path(data_dir, "performance_criteria.csv"))

weights <- setNames(criteria$weight, criteria$criterion_name)

rows <- list()
row_index <- 1

clamp <- function(x) {
  max(0, min(1, x))
}

for (i in seq_len(nrow(scenarios))) {
  scenario <- scenarios[i, ]
  for (j in seq_len(nrow(strategies))) {
    strategy <- strategies[j, ]

    effectiveness <- clamp(
      strategy$baseline_effectiveness -
        0.22 * scenario$disruption_level +
        0.26 * strategy$shock_absorption -
        0.08 * scenario$ecological_stress -
        0.05 * scenario$technology_volatility * (1 - strategy$adaptability)
    )

    feasibility <- clamp(
      scenario$implementation_capacity +
        0.18 * scenario$fiscal_capacity -
        0.30 * strategy$implementation_complexity -
        0.05 * scenario$disruption_level
    )

    legitimacy <- clamp(
      0.40 * scenario$public_trust +
        0.25 * strategy$legitimacy_design +
        0.20 * strategy$equity_quality +
        0.15 * strategy$adaptability -
        0.05 * scenario$distributional_pressure
    )

    equity <- clamp(
      strategy$equity_quality -
        0.30 * scenario$distributional_pressure +
        0.15 * strategy$legitimacy_design +
        0.10 * strategy$transformability
    )

    adaptability_score <- clamp(
      0.70 * strategy$adaptability +
        0.30 * scenario$implementation_capacity -
        0.05 * scenario$technology_volatility * (1 - strategy$shock_absorption)
    )

    transformability_score <- clamp(
      0.70 * strategy$transformability +
        0.30 * strategy$legitimacy_design -
        0.06 * strategy$implementation_complexity
    )

    viability <- clamp(
      weights["effectiveness"] * effectiveness +
        weights["feasibility"] * feasibility +
        weights["legitimacy"] * legitimacy +
        weights["equity"] * equity +
        weights["adaptability"] * adaptability_score +
        weights["transformability"] * transformability_score
    )

    rows[[row_index]] <- data.frame(
      scenario_id = scenario$scenario_id,
      scenario_name = scenario$scenario_name,
      strategy_id = strategy$strategy_id,
      strategy_name = strategy$strategy_name,
      effectiveness = round(effectiveness, 4),
      feasibility = round(feasibility, 4),
      legitimacy = round(legitimacy, 4),
      equity = round(equity, 4),
      adaptability_score = round(adaptability_score, 4),
      transformability_score = round(transformability_score, 4),
      viability_score = round(viability, 4)
    )

    row_index <- row_index + 1
  }
}

performance <- do.call(rbind, rows)

summary_rows <- list()
summary_index <- 1

for (strategy_id in unique(performance$strategy_id)) {
  subset <- performance[performance$strategy_id == strategy_id, ]
  scores <- subset$viability_score

  summary_rows[[summary_index]] <- data.frame(
    strategy_id = strategy_id,
    strategy_name = subset$strategy_name[1],
    worst_case_viability = round(min(scores), 4),
    mean_viability = round(mean(scores), 4),
    best_case_viability = round(max(scores), 4),
    viability_range = round(max(scores) - min(scores), 4),
    threshold_failures = sum(scores < 0.50)
  )
  summary_index <- summary_index + 1
}

robustness <- do.call(rbind, summary_rows)
robustness <- robustness[order(-robustness$worst_case_viability, -robustness$mean_viability), ]

regret_rows <- list()
regret_index <- 1

for (scenario_id in unique(performance$scenario_id)) {
  subset <- performance[performance$scenario_id == scenario_id, ]
  best_score <- max(subset$viability_score)

  for (i in seq_len(nrow(subset))) {
    regret_rows[[regret_index]] <- data.frame(
      scenario_id = subset$scenario_id[i],
      scenario_name = subset$scenario_name[i],
      strategy_id = subset$strategy_id[i],
      strategy_name = subset$strategy_name[i],
      viability_score = subset$viability_score[i],
      best_scenario_viability = best_score,
      regret = round(best_score - subset$viability_score[i], 4)
    )
    regret_index <- regret_index + 1
  }
}

regret <- do.call(rbind, regret_rows)

regret_summary_rows <- list()
regret_summary_index <- 1

for (strategy_id in unique(regret$strategy_id)) {
  subset <- regret[regret$strategy_id == strategy_id, ]
  regret_summary_rows[[regret_summary_index]] <- data.frame(
    strategy_id = strategy_id,
    strategy_name = subset$strategy_name[1],
    max_regret = round(max(subset$regret), 4),
    mean_regret = round(mean(subset$regret), 4)
  )
  regret_summary_index <- regret_summary_index + 1
}

regret_summary <- do.call(rbind, regret_summary_rows)
regret_summary <- regret_summary[order(regret_summary$max_regret, regret_summary$mean_regret), ]

write.csv(performance, file.path(outputs_dir, "r_scenario_strategy_performance.csv"), row.names = FALSE)
write.csv(robustness, file.path(outputs_dir, "r_strategy_robustness_scores.csv"), row.names = FALSE)
write.csv(regret, file.path(outputs_dir, "r_scenario_strategy_regret.csv"), row.names = FALSE)
write.csv(regret_summary, file.path(outputs_dir, "r_strategy_regret_summary.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_strategy_robustness_scores.png"), width = 1200, height = 800)
barplot(
  robustness$worst_case_viability,
  names.arg = robustness$strategy_name,
  horiz = TRUE,
  las = 1,
  main = "Worst-Case Strategy Viability Across Futures",
  xlab = "Worst-case viability"
)
dev.off()

print(robustness)
print(regret_summary)
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
