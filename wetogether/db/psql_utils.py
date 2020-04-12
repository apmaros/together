import psycopg2

from wetogether.db import DbConfig


def psql_connect(config: DbConfig):
    return psycopg2.connect(
        user=config.username,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.database
    )
