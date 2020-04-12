import logging

import falcon

from api.routes import set_routes
from api.server import Server
from config.api_config import get_server_config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info("starting Together API")
    config = get_server_config()
    api = falcon.API()
    server = Server()
    server.start(config, set_routes(api))
    logger.info("started Together API")
