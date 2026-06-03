#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Future Consumer Behavior and Market Change..."

python3 python/consumer_market_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  echo "Running R workflow..."
  Rscript r/consumer_market_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  echo "Testing SQL schema..."
  rm -f outputs/consumer_market_futures_schema.db
  sqlite3 outputs/consumer_market_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  echo "Running Julia workflow..."
  julia julia/consumer_future_health.jl > outputs/julia_consumer_future_health_scores.csv
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  echo "Running Go workflow..."
  (cd go && go run main.go) > outputs/go_consumer_future_health_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  echo "Running Rust workflow..."
  (cd rust && cargo run --quiet) > outputs/rust_consumer_future_health_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v g++ >/dev/null 2>&1; then
  echo "Running C++ workflow..."
  g++ cpp/consumer_future_health.cpp -o outputs/consumer_future_health_cpp
  ./outputs/consumer_future_health_cpp > outputs/cpp_consumer_future_health_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gcc >/dev/null 2>&1; then
  echo "Running C workflow..."
  gcc c/consumer_future_health.c -o outputs/consumer_future_health_c
  ./outputs/consumer_future_health_c > outputs/c_consumer_future_health_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  echo "Running Fortran workflow..."
  gfortran fortran/consumer_future_health.f90 -o outputs/consumer_future_health_fortran
  ./outputs/consumer_future_health_fortran > outputs/fortran_consumer_future_health_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

echo ""
echo "Smoke tests complete."
echo "Generated outputs:"
find outputs -maxdepth 1 -type f | sort
