from falcon import API
from falcon_auth import FalconAuthMiddleware
from sqlalchemy.orm import Session

from api.middleware.JwtAuth import JwtAuth
from api.middleware.json_translator import JSONTranslator
from api.middleware.require_json import RequireJSON
from api.routes import set_routes
from config.jwt_config import jwt_config


def get_api(db: Session) -> API:
    api = __build_api(db)
    return set_routes(api, db)


def __build_api(db: Session) -> API:
    api = API(
        middleware=[
            RequireJSON(),
            JSONTranslator(),
            FalconAuthMiddleware(
                JwtAuth(jwt_config, db).get_backend(),
                [],
                ['HEAD']
            )
        ]
    )
    api.req_options.auto_parse_form_urlencoded = True
    return api
