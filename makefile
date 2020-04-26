# must use TABS instead of spaces
# otherwise fails with makefile:X: *** missing separator.  Stop.
run:
	python ./wetogether/app.py
migrate:
	./bin/migrate_db.sh
