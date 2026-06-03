# Base R workflow for AI and the Future of Decision-Making.
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

systems <- read.csv(file.path(data_dir, "decision_system_profiles.csv"))
governance <- read.csv(file.path(data_dir, "governance_controls.csv"))
equity <- read.csv(file.path(data_dir, "equity_harm_indicators.csv"))

systems$decision_system_profile_score <- round(
  0.16 * systems$human_judgment +
  0.16 * systems$machine_inference +
  0.16 * systems$coordination_quality +
  0.12 * systems$transparency +
  0.12 * systems$uncertainty_management +
  0.12 * systems$accountability +
  0.08 * systems$contestability +
  0.08 * systems$equity_protection,
  4
)

systems$governance_profile_score <- round(
  0.22 * systems$transparency +
  0.24 * systems$accountability +
  0.24 * systems$contestability +
  0.18 * systems$uncertainty_management +
  0.12 * systems$equity_protection,
  4
)

systems$risk_profile_score <- round(
  0.26 * systems$automation_intensity +
  0.20 * (1 - systems$accountability) +
  0.20 * (1 - systems$contestability) +
  0.18 * (1 - systems$transparency) +
  0.16 * (1 - systems$equity_protection),
  4
)

systems <- systems[order(-systems$decision_system_profile_score), ]

governance$governance_readiness_score <- round(
  0.16 * governance$documentation +
  0.16 * governance$auditability +
  0.14 * governance$explainability +
  0.16 * governance$human_oversight +
  0.14 * governance$appeal_rights +
  0.12 * governance$monitoring_strength +
  0.12 * governance$enforcement_capacity,
  4
)

governance$governance_gap_score <- round(1 - governance$governance_readiness_score, 4)
governance <- governance[order(-governance$governance_gap_score), ]

equity$justice_capacity_score <- round(
  0.18 * equity$contestability +
  0.18 * equity$voice +
  0.20 * equity$protection +
  0.18 * equity$repair_capacity +
  0.14 * (1 - equity$error_burden) +
  0.12 * (1 - equity$vulnerability),
  4
)

equity$harm_risk_score <- round(
  0.25 * equity$error_burden +
  0.22 * equity$exposure +
  0.22 * equity$vulnerability +
  0.16 * (1 - equity$contestability) +
  0.15 * (1 - equity$repair_capacity),
  4
)

equity <- equity[order(-equity$harm_risk_score), ]

write.csv(systems, file.path(outputs_dir, "r_decision_system_profile_scores.csv"), row.names = FALSE)
write.csv(governance, file.path(outputs_dir, "r_governance_readiness_scores.csv"), row.names = FALSE)
write.csv(equity, file.path(outputs_dir, "r_equity_harm_scores.csv"), row.names = FALSE)

png(file.path(outputs_dir, "r_decision_system_profile_scores.png"), width = 1200, height = 800)
barplot(
  systems$decision_system_profile_score,
  names.arg = systems$system_type,
  horiz = TRUE,
  las = 1,
  main = "AI Decision-System Profile Scores",
  xlab = "Decision-system profile"
)
dev.off()

png(file.path(outputs_dir, "r_governance_gap_scores.png"), width = 1200, height = 800)
barplot(
  governance$governance_gap_score,
  names.arg = governance$control_name,
  horiz = TRUE,
  las = 1,
  main = "AI Governance Gap Scores",
  xlab = "Governance gap"
)
dev.off()

print(systems[, c("system_id", "system_type", "decision_system_profile_score", "governance_profile_score", "risk_profile_score")])
print(governance[, c("control_id", "control_name", "governance_readiness_score", "governance_gap_score")])
cat("R workflow complete. Outputs written to:", outputs_dir, "\n")
