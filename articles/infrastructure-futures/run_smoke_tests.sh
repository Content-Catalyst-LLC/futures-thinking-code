#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Infrastructure Futures..."

python3 python/infrastructure_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/infrastructure_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/infrastructure_futures_schema.db
  sqlite3 outputs/infrastructure_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/infrastructure_viability.jl > outputs/julia_infrastructure_viability_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_infrastructure_viability_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_infrastructure_viability_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/infrastructure_viability.cpp -o outputs/infrastructure_viability_cpp
  ./outputs/infrastructure_viability_cpp > outputs/cpp_infrastructure_viability_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/infrastructure_viability.c -o outputs/infrastructure_viability_c
  ./outputs/infrastructure_viability_c > outputs/c_infrastructure_viability_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/infrastructure_viability.f90 -o outputs/infrastructure_viability_fortran
  ./outputs/infrastructure_viability_fortran > outputs/fortran_infrastructure_viability_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
