#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Societal Transformation and Long-Term Change..."

python3 python/societal_transformation_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/societal_transformation_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/societal_transformation_schema.db
  sqlite3 outputs/societal_transformation_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/transformation_capacity.jl > outputs/julia_transformation_capacity.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_transformation_capacity_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_transformation_capacity_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/transformation_capacity.cpp -o outputs/transformation_capacity_cpp
  ./outputs/transformation_capacity_cpp > outputs/cpp_transformation_capacity_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/transformation_capacity.c -o outputs/transformation_capacity_c
  ./outputs/transformation_capacity_c > outputs/c_transformation_capacity_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/transformation_capacity.f90 -o outputs/transformation_capacity_fortran
  ./outputs/transformation_capacity_fortran > outputs/fortran_transformation_capacity_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
