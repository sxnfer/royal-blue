#!/usr/bin/env bash

REPO_ROOT="$(git rev-parse --show-toplevel)"
for file in "${REPO_ROOT}/sql"/*.sql; do
    psql -f "${file}" > ${file%.sql}.txt
done