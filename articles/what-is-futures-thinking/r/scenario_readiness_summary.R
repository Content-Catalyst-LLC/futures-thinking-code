# Futures Thinking: Scenario Readiness Summary in R
# Educational example only.

library(tidyverse)

performance <- read_csv("../data/strategy_future_performance.csv", show_col_types = FALSE)

summary <- performance |>
  group_by(strategy) |>
  summarise(
    mean_performance = mean(performance),
    worst_case = min(performance),
    best_case = max(performance),
    performance_range = max(performance) - min(performance),
    .groups = "drop"
  ) |>
  mutate(
    robustness_score =
      0.50 * worst_case +
      0.30 * mean_performance -
      0.20 * performance_range
  ) |>
  arrange(desc(robustness_score))

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(summary, "../outputs/r_strategy_readiness_summary.csv")

print(summary)
