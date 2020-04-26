#!/bin/bash
echo `date` initiated application start

source bin/init_dev_env.sh
./bin/migrate_db.sh
python wetogether/app.py
