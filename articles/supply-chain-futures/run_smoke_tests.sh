#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Supply Chain Futures..."

python3 python/supply_chain_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/supply_chain_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/supply_chain_futures_schema.db
  sqlite3 outputs/supply_chain_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/supply_chain_resilience.jl > outputs/julia_supply_chain_resilience_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_supply_chain_resilience_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_supply_chain_resilience_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/supply_chain_resilience.cpp -o outputs/supply_chain_resilience_cpp
  ./outputs/supply_chain_resilience_cpp > outputs/cpp_supply_chain_resilience_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/supply_chain_resilience.c -o outputs/supply_chain_resilience_c
  ./outputs/supply_chain_resilience_c > outputs/c_supply_chain_resilience_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/supply_chain_resilience.f90 -o outputs/supply_chain_resilience_fortran
  ./outputs/supply_chain_resilience_fortran > outputs/fortran_supply_chain_resilience_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
