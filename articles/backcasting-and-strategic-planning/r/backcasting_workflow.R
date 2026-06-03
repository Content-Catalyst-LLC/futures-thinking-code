# Base R workflow for Backcasting and Strategic Planning.
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

pathways <- read.csv(file.path(data_dir, "pathways.csv"))
milestones <- read.csv(file.path(data_dir, "milestones.csv"))
constraints <- read.csv(file.path(data_dir, "constraints.csv"))

pathways$pathway_viability_score <- round(
  0.18 * pathways$feasibility -
  0.16 * pathways$institutional_difficulty +
  0.14 * pathways$transition_speed +
  0.18 * pathways$stakeholder_alignment +
  0.16 * pathways$resilience +
  0.12 * pathways$justice +
  0.14 * pathways$adaptability -
  0.12 * pathways$political_friction,
  4
)

pathways$pathway_class <- ifelse(
  pathways$pathway_viability_score >= 0.55,
  "Strong adaptive pathway",
  ifelse(
    pathways$pathway_viability_score >= 0.45,
    "Potential pathway with constraints",
    "Fragile or high-risk pathway"
  )
)

pathways <- pathways[order(-pathways$pathway_viability_score), ]

milestones$milestone_risk_priority <- round(
  milestones$risk_score * (1 - milestones$completion_score),
  4
)
milestones <- milestones[order(-milestones$milestone_risk_priority), ]

constraints$constraint_priority <- round(
  constraints$impact * constraints$severity * (1 + (1 - constraints$reversibility)),
  4
)
constraints <- constraints[order(-constraints$constraint_priority), ]

write.csv(pathways, file.path(outputs_dir, "r_pathway_viability_scores.csv"), row.names = FALSE)
write.csv(milestones, file.path(outputs_dir, "r_milestone_risk_priorities.csv"), row.names = FALSE)
write.csv(constraints, file.path(outputs_dir, "r_constraint_priorities.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_pathway_viability_scores.png"), width = 1200, height = 800)
barplot(
  pathways$pathway_viability_score,
  names.arg = pathways$pathway_name,
  horiz = TRUE,
  las = 1,
  main = "Backcasting Pathway Viability Scores",
  xlab = "Viability score"
)
dev.off()

print(pathways[, c("pathway_name", "future_id", "pathway_viability_score", "pathway_class")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
