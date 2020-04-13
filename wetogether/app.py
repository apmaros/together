import logging

from api.routes import set_routes
from api.server import Server, get_api
from config.api_config import get_server_config
from config.db_config import DbConfig
from db.session import get_session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def run():
    logger.info("starting Together API")
    db_session = get_session(DbConfig())
    api_routes = set_routes(get_api(), db_session)
    config = get_server_config()
    Server().start(config, api_routes)
    logger.info("started Together API")


if __name__ == '__main__':
    run()
