#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Food, Water, and Land-Use Futures..."

python3 python/food_water_land_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/food_water_land_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/food_water_land_schema.db
  sqlite3 outputs/food_water_land_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/food_water_land_resilience.jl > outputs/julia_food_water_land_resilience_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_food_water_land_resilience_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_food_water_land_resilience_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/food_water_land_resilience.cpp -o outputs/food_water_land_resilience_cpp
  ./outputs/food_water_land_resilience_cpp > outputs/cpp_food_water_land_resilience_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/food_water_land_resilience.c -o outputs/food_water_land_resilience_c
  ./outputs/food_water_land_resilience_c > outputs/c_food_water_land_resilience_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/food_water_land_resilience.f90 -o outputs/food_water_land_resilience_fortran
  ./outputs/food_water_land_resilience_fortran > outputs/fortran_food_water_land_resilience_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
