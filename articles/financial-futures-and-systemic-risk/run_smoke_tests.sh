#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Financial Futures and Systemic Risk..."

python3 python/financial_futures_systemic_risk_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/financial_futures_systemic_risk_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/financial_futures_systemic_risk_schema.db
  sqlite3 outputs/financial_futures_systemic_risk_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/financial_resilience.jl > outputs/julia_financial_resilience_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_financial_resilience_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_financial_resilience_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/financial_resilience.cpp -o outputs/financial_resilience_cpp
  ./outputs/financial_resilience_cpp > outputs/cpp_financial_resilience_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/financial_resilience.c -o outputs/financial_resilience_c
  ./outputs/financial_resilience_c > outputs/c_financial_resilience_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/financial_resilience.f90 -o outputs/financial_resilience_fortran
  ./outputs/financial_resilience_fortran > outputs/fortran_financial_resilience_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
