# Base R workflow for The History of Futures Thinking.
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

traditions <- read.csv(file.path(data_dir, "historical_traditions.csv"))
methods <- read.csv(file.path(data_dir, "method_genealogy.csv"))

traditions$reflective_foresight_score <- round(
  0.25 * traditions$methodological_discipline +
  0.25 * traditions$participatory_depth +
  0.25 * traditions$ethical_reflection +
  0.25 * traditions$systems_orientation,
  4
)

traditions$power_risk_score <- round(
  traditions$institutional_power *
  (1 - traditions$participatory_depth) *
  (1 - traditions$ethical_reflection),
  4
)

traditions <- traditions[order(-traditions$reflective_foresight_score), ]

methods$method_risk_score <- round(
  methods$technocratic_risk *
  (1 - methods$participatory_potential) *
  (1 - methods$ethical_sensitivity),
  4
)

methods$reflective_method_score <- round(
  0.34 * methods$participatory_potential +
  0.33 * methods$ethical_sensitivity +
  0.33 * (1 - methods$technocratic_risk),
  4
)

methods <- methods[order(-methods$reflective_method_score), ]

write.csv(traditions, file.path(outputs_dir, "r_historical_tradition_scores.csv"), row.names = FALSE)
write.csv(methods, file.path(outputs_dir, "r_method_genealogy_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_historical_tradition_scores.png"), width = 1100, height = 700)
barplot(
  traditions$reflective_foresight_score,
  names.arg = traditions$tradition,
  horiz = TRUE,
  las = 1,
  main = "Reflective Foresight Score by Historical Tradition",
  xlab = "Reflective foresight score"
)
dev.off()

print(traditions[, c("tradition", "reflective_foresight_score", "power_risk_score")])
print(methods[, c("method", "reflective_method_score", "method_risk_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
