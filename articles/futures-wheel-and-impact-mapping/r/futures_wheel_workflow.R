# Base R workflow for Futures Wheel and Impact Mapping.
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

consequences <- read.csv(file.path(data_dir, "consequence_nodes.csv"))
pathways <- read.csv(file.path(data_dir, "impact_pathways.csv"))
distribution <- read.csv(file.path(data_dir, "distributional_audit.csv"))

consequences$priority_score <- round(
  0.22 * consequences$likelihood +
  0.26 * consequences$severity +
  0.14 * consequences$uncertainty +
  0.22 * consequences$distributional_burden +
  0.16 * consequences$actionability,
  4
)

consequences$priority_class <- ifelse(
  consequences$priority_score >= 0.82,
  "High-priority cascade",
  ifelse(
    consequences$priority_score >= 0.74,
    "Monitor and prepare",
    "Context-dependent priority"
  )
)

consequences <- consequences[order(-consequences$priority_score), ]

pathways$impact_pathway_score <- round(
  0.40 * pathways$traceability_score +
  0.30 * pathways$equity_relevance +
  0.30 * pathways$implementation_feasibility,
  4
)
pathways <- pathways[order(-pathways$impact_pathway_score), ]

distribution$distributional_risk_score <- round(
  0.35 * distribution$exposure +
  0.30 * (1 - distribution$adaptive_capacity) +
  0.20 * (1 - distribution$decision_voice) +
  0.15 * distribution$burden_shift_risk,
  4
)
distribution <- distribution[order(-distribution$distributional_risk_score), ]

write.csv(consequences, file.path(outputs_dir, "r_consequence_priority_scores.csv"), row.names = FALSE)
write.csv(pathways, file.path(outputs_dir, "r_impact_pathway_scores.csv"), row.names = FALSE)
write.csv(distribution, file.path(outputs_dir, "r_distributional_risk_scores.csv"), row.names = FALSE)

plot_data <- consequences[consequences$consequence_order > 0, ]
plot_data <- plot_data[order(plot_data$priority_score), ]

png(file.path(outputs_dir, "r_consequence_priority_scores.png"), width = 1200, height = 800)
barplot(
  plot_data$priority_score,
  names.arg = plot_data$consequence,
  horiz = TRUE,
  las = 1,
  main = "Futures Wheel Consequence Priority Scores",
  xlab = "Priority score"
)
dev.off()

print(consequences[, c("node_id", "consequence_order", "consequence", "domain", "priority_score", "priority_class")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
