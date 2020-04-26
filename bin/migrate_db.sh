#!/usr/bin/env bash
set -euo pipefail

echo `date` migrating database

alembic upgrade head

echo `date` migration succesfully finished
