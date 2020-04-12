run:
	python ./wetogether/app.py
migrate:
	alembic upgrade head
