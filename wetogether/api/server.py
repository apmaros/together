import logging
from wsgiref import simple_server

from config.api_config import ServerConfig


class Server:
    logger = logging.getLogger(__name__)
    server = simple_server

    def start(self, config: ServerConfig, api):
        self.logger.info(f'starting server listening on {config.host}:{config.port}')

        httpd = self.server.make_server(
            config.host,
            config.port,
            api
        )

        # seems it creates only one worker
        httpd.serve_forever()
        self.logger.info("server started")
