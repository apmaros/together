# must use TABS instead of spaces
# otherwise fails with makefile:X: *** missing separator.  Stop.
run:
	python ./src/main/together/app.py
migrate:
	./bin/migrate_db.sh
test:
    ./bin/test.sh
