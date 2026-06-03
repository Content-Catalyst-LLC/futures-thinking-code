#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Democratic Futures and Public Participation..."

python3 python/democratic_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/democratic_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/democratic_futures_schema.db
  sqlite3 outputs/democratic_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/democratic_capacity.jl > outputs/julia_democratic_capacity_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_democratic_capacity_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_democratic_capacity_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/democratic_capacity.cpp -o outputs/democratic_capacity_cpp
  ./outputs/democratic_capacity_cpp > outputs/cpp_democratic_capacity_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/democratic_capacity.c -o outputs/democratic_capacity_c
  ./outputs/democratic_capacity_c > outputs/c_democratic_capacity_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/democratic_capacity.f90 -o outputs/democratic_capacity_fortran
  ./outputs/democratic_capacity_fortran > outputs/fortran_democratic_capacity_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
