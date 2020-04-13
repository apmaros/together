import os
import string
from dataclasses import dataclass


@dataclass
class DbConfig:
    username: string
    password: string
    host: string
    port: int
    database: string

    def __init__(
            self,
            username=os.environ["DB_USERNAME"],
            password=os.environ["DB_PASSWORD"],
            host=os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            database=os.environ["DB_NAME"]
    ):
        self.username=username
        self.password=password
        self.host=host
        self.port=port
        self.database=database


def get_db_url(config: DbConfig = DbConfig()):
    return "postgresql://{}:{}@{}:{}/{}".format(
        config.username,
        config.password,
        config.host,
        config.port,
        config.database,
    )
