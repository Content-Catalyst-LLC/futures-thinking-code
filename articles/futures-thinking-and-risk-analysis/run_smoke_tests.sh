#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Futures Thinking and Risk Analysis..."

python3 python/futures_risk_analysis_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/futures_risk_analysis_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/futures_risk_analysis_schema.db
  sqlite3 outputs/futures_risk_analysis_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/risk_profile_score.jl > outputs/julia_risk_profile_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_futures_risk_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_futures_risk_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/futures_risk_score.cpp -o outputs/futures_risk_cpp
  ./outputs/futures_risk_cpp > outputs/cpp_futures_risk_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/futures_risk_score.c -o outputs/futures_risk_c
  ./outputs/futures_risk_c > outputs/c_futures_risk_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/futures_risk_score.f90 -o outputs/futures_risk_fortran
  ./outputs/futures_risk_fortran > outputs/fortran_futures_risk_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
