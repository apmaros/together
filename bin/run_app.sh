#!/bin/bash
echo `date` initiated application start

source bin/init_env.sh
time ./bin/migrate_db.sh
python wetogether/app.py
