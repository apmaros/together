import logging
from wsgiref import simple_server
from falcon import API
from config.api_config import ServerConfig
from api.middleware.json_translator import JSONTranslator
from api.middleware.require_json import RequireJSON


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
