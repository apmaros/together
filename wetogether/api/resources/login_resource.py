import logging
import string
from datetime import datetime, timedelta

import falcon
from falcon import json
import jwt
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from api.resources.util import get_param
from api.security import verify_secret
from config.jwt_config import JwtConfig, jwt_config
from model.user import User


class LoginResource(object):
    logger = logging.getLogger(__name__)

    def on_post(self, req, resp):
        email = get_param(req, 'email')
        password = get_param(req, 'password')

        if email is None or password is None:
            resp.body = json.dumps({'error': 'One or more values is missing'})
            resp.status = falcon.HTTP_401
            return
        try:
            user = self.db.query(User).filter(User.email == email).one()
            if verify_secret(password, user.password):
                payload = {
                    'user_id': str(user.id),
                    'exp': datetime.utcnow() + timedelta(
                        hours=self.jwt_config.expire_delta_hours
                    )
                }
                jwt_token = jwt.encode(
                    payload,
                    self.jwt_config.secret,
                    self.jwt_config.algorithm
                )
                resp.body = json.dumps({'token': jwt_token.decode('utf-8')})

        except NoResultFound:
            self.logger.debug('user not found')
            set_invalid_credentials(resp)
        except ValueError:
            self.logger.debug('cant verify password')
            set_invalid_credentials(resp)

    def __init__(self, db: Session):
        self.jwt_config = jwt_config
        self.db: Session = db


def set_invalid_credentials(resp):
    resp.body = json.dumps({'error': 'Credentials are not valid'})
    resp.status = falcon.HTTP_400
