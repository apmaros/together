#!/usr/bin/env bash
echo `date` migrating database

alembic upgrade head
