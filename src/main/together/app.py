import logging

from api.api_manager import get_api
from api.server import Server
from config.api_config import get_server_config
from config.db_config import DbConfig
from db.session import get_session

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-15s %(message)s')


def run():
    logger.info("starting Together API")
    db_session = get_session(DbConfig())
    config = get_server_config()
    api = get_api(db_session)
    Server().start(config, api)
    logger.info("started Together API")


if __name__ == '__main__':
    run()
