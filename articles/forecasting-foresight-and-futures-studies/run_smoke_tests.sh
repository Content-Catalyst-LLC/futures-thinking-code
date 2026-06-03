#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests..."

python3 python/futures_workflow_standard.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/futures_profiles.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/uncertainty_robustness.jl > outputs/julia_robustness_output.txt
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  sqlite3 outputs/futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_diagnostics_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_diagnostics_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/scenario_performance.cpp -o outputs/scenario_performance_cpp
  ./outputs/scenario_performance_cpp > outputs/cpp_diagnostics_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/scenario_score.c -lm -o outputs/scenario_score_c
  ./outputs/scenario_score_c > outputs/c_diagnostics_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/readiness.f90 -o outputs/readiness_fortran
  ./outputs/readiness_fortran > outputs/fortran_readiness_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Outputs are in: outputs/"
