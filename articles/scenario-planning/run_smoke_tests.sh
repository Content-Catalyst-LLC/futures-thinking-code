#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Scenario Planning..."

python3 python/scenario_planning_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/scenario_planning_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  sqlite3 outputs/scenario_planning_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/scenario_robustness.jl > outputs/julia_scenario_robustness.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_scenario_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_scenario_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/scenario_robustness.cpp -o outputs/scenario_robustness_cpp
  ./outputs/scenario_robustness_cpp > outputs/cpp_scenario_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/scenario_score.c -lm -o outputs/scenario_score_c
  ./outputs/scenario_score_c > outputs/c_scenario_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/scenario_readiness.f90 -o outputs/scenario_readiness_fortran
  ./outputs/scenario_readiness_fortran > outputs/fortran_scenario_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
