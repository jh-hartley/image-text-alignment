#!/bin/bash

set -euo pipefail

LINE_LENGTH=79

log() { echo "==> $1"; }

error() {
    echo "ERROR: $1" >&2
    exit 1
}

run_check() {
    local name=$1
    local cmd=$2
    local fix_cmd=$3

    log "Running $name..."
    if ! eval "$cmd"; then
        error "$name check failed"
        if [ -n "$fix_cmd" ]; then
            echo "Run '$fix_cmd' to automatically fix the issues"
        fi
    fi
}

main() {
    local fix_mode=false
    if [ "${1:-}" == "--fix" ]; then
        fix_mode=true
    fi

    log "Running code quality checks..."

    if [ "$fix_mode" = true ]; then
        log "Fixing import sorting..."
        isort .
        log "Fixing black formatting..."
        black .
        log "Fixing ruff issues..."
        ruff check . --fix
    else
        run_check "black" \
            "black . --check --verbose --line-length $LINE_LENGTH" \
            "./scripts/check.sh --fix"

        run_check "isort" \
            "isort . --check-only --diff" \
            "./scripts/check.sh --fix"

        run_check "ruff" \
            "ruff check ." \
            "./scripts/check.sh --fix"
    fi

    run_check "mypy" \
        "mypy src/ --show-error-codes" \
        ""

    if find tests/ -name "test_*.py" -type f -print -quit | grep -q .; then
        run_check "tests" \
            "pytest tests/ -v" \
            ""
    else
        log "No test files found, skipping tests"
    fi

    log "All checks passed! ✨"
}

main "$@" 