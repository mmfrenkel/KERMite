#!/bin/bash

run_type_d="all"
test_dir_d="./server/tests"
report_dir_d="./reports/backend/tests"

if [ "-h" = "$1" ] || [ "--help" = "$1" ]; then
    echo "Usage: $0 [run_type] [test_dir] [report_dir]"
    echo "Defaults: run_type = $run_type_d, test_dir = $test_dir_d, report_dir = $report_dir_d"
    exit
fi

run_type="${1:-$run_type_d}"
test_dir="${2:-$test_dir_d}"
report_dir="${3:-$report_dir_d}"

current_time="$(date --utc "+%FT%TZ")"
filename="$run_type-$current_time.txt"

python -m pytest -v "$test_dir/$1" 2>&1 | tee "$report_dir/$filename"
