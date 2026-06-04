#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Futures Thinking and Sustainability..."

python3 python/sustainability_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/sustainability_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/sustainability_futures_schema.db
  sqlite3 outputs/sustainability_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/sustainability_viability.jl > outputs/julia_sustainability_viability_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_sustainability_viability_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_sustainability_viability_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/sustainability_viability.cpp -o outputs/sustainability_viability_cpp
  ./outputs/sustainability_viability_cpp > outputs/cpp_sustainability_viability_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/sustainability_viability.c -o outputs/sustainability_viability_c
  ./outputs/sustainability_viability_c > outputs/c_sustainability_viability_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/sustainability_viability.f90 -o outputs/sustainability_viability_fortran
  ./outputs/sustainability_viability_fortran > outputs/fortran_sustainability_viability_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
