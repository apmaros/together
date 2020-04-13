import os
import string
from dataclasses import dataclass


@dataclass
class ServerConfig:
    host: string = '127.0.0.1'
    port: int = 8080


def get_server_config() -> ServerConfig:
    return ServerConfig(
        os.environ["API_HOST"],
        int(os.environ["API_PORT"])
    )
