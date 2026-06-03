# Base R workflow for Futures Literacy and Anticipatory Capacity.
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

profiles <- read.csv(file.path(data_dir, "capacity_profiles.csv"))
assumptions <- read.csv(file.path(data_dir, "assumptions.csv"))
signals <- read.csv(file.path(data_dir, "signals.csv"))

weights <- c(
  scanning_capacity = 0.15,
  interpretive_capacity = 0.15,
  assumption_visibility = 0.17,
  imagination_range = 0.13,
  participatory_depth = 0.17,
  learning_capacity = 0.13,
  action_translation = 0.10
)

profiles$anticipatory_capacity_score <- 0
for (dimension in names(weights)) {
  profiles$anticipatory_capacity_score <- profiles$anticipatory_capacity_score + profiles[[dimension]] * weights[[dimension]]
}
profiles$anticipatory_capacity_score <- round(profiles$anticipatory_capacity_score, 4)
profiles <- profiles[order(-profiles$anticipatory_capacity_score), ]

assumptions$vulnerability_score <- round(
  assumptions$exposure * (1 - assumptions$confidence) * (1 + (1 - assumptions$reversibility)),
  4
)
assumptions <- assumptions[order(-assumptions$vulnerability_score), ]

signals$watch_score <- round(
  0.35 * signals$uncertainty + 0.40 * signals$impact + 0.25 * signals$novelty,
  4
)
signals <- signals[order(-signals$watch_score), ]

write.csv(profiles, file.path(outputs_dir, "r_anticipatory_capacity_scores.csv"), row.names = FALSE)
write.csv(assumptions, file.path(outputs_dir, "r_assumption_vulnerability_scores.csv"), row.names = FALSE)
write.csv(signals, file.path(outputs_dir, "r_signal_watch_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_anticipatory_capacity_scores.png"), width = 1100, height = 700)
barplot(
  profiles$anticipatory_capacity_score,
  names.arg = profiles$organization_type,
  horiz = TRUE,
  las = 1,
  main = "Anticipatory Capacity Scores",
  xlab = "Weighted score"
)
dev.off()

print(profiles[, c("organization_type", "anticipatory_capacity_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
