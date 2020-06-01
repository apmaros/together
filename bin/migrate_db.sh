#!/usr/bin/env bash
set -euo pipefail

export PYTHONPATH=./src/main/together

echo `date` migrating database

alembic upgrade head

echo `date` migration succesfully finished
