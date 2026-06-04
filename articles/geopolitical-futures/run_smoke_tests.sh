#!/usr/bin/env bash
set -euo pipefail

echo "Running smoke tests for Geopolitical Futures..."

python3 python/geopolitical_futures_workflow.py

if command -v Rscript >/dev/null 2>&1; then
  Rscript r/geopolitical_futures_workflow.R
else
  echo "Skipping R workflow: Rscript not found."
fi

if command -v sqlite3 >/dev/null 2>&1; then
  rm -f outputs/geopolitical_futures_schema.db
  sqlite3 outputs/geopolitical_futures_schema.db < sql/schema.sql
else
  echo "Skipping SQL schema test: sqlite3 not found."
fi

if command -v julia >/dev/null 2>&1; then
  julia julia/geopolitical_stability.jl > outputs/julia_geopolitical_stability_output.txt
else
  echo "Skipping Julia workflow: julia not found."
fi

if command -v go >/dev/null 2>&1; then
  (cd go && go run main.go) > outputs/go_geopolitical_stability_output.txt
else
  echo "Skipping Go workflow: go not found."
fi

if command -v cargo >/dev/null 2>&1; then
  (cd rust && cargo run --quiet) > outputs/rust_geopolitical_stability_output.txt
else
  echo "Skipping Rust workflow: cargo not found."
fi

if command -v gcc >/dev/null 2>&1; then
  gcc c/geopolitical_stability.c -o outputs/geopolitical_stability_c
  ./outputs/geopolitical_stability_c > outputs/c_geopolitical_stability_output.txt
else
  echo "Skipping C workflow: gcc not found."
fi

if command -v g++ >/dev/null 2>&1; then
  g++ cpp/geopolitical_stability.cpp -o outputs/geopolitical_stability_cpp
  ./outputs/geopolitical_stability_cpp > outputs/cpp_geopolitical_stability_output.txt
else
  echo "Skipping C++ workflow: g++ not found."
fi

if command -v gfortran >/dev/null 2>&1; then
  gfortran fortran/geopolitical_stability.f90 -o outputs/geopolitical_stability_fortran
  ./outputs/geopolitical_stability_fortran > outputs/fortran_geopolitical_stability_output.txt
else
  echo "Skipping Fortran workflow: gfortran not found."
fi

test -f outputs/geopolitical_futures_report.md
echo "Smoke tests complete."
find outputs -maxdepth 1 -type f | sort
