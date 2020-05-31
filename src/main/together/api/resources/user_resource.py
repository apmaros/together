import json
import logging
import falcon
from sqlalchemy import func
from sqlalchemy.orm import Session
from api.resources.util import get_param
from api.security import hash
from db.data_access.user import save_user
from model.user import User


class UserResource(object):
    logger = logging.getLogger(__name__)

    auth = {
        'exempt_methods': ['POST']
    }

    def on_get(self, req, resp):
        user = req.context['user'].pop()
        logging.info(f'user={user}')

        resp.body = json.dumps({
            'id': str(user.id),
            'email': user.email,
            'created_at': user.created_at.timestamp(),
        })
        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        username = get_param(req, 'username')
        email = get_param(req, 'email')
        firstname = get_param(req, 'firstname')
        lastname = get_param(req, 'lastname')
        password = get_param(req, 'password')

        if username is None or email is None or password is None:
            resp.body = json.dumps(
                {'error': 'One or more required values are missing'}
            )
            resp.status = falcon.HTTP_401
            return

        user = User(
            username=username,
            email=email,
            first_name=firstname,
            last_name=lastname,
            password=hash(password),
            created_at=func.now(),
            last_access_at=None
        )

        save_user(self.db, user)

        resp.status = falcon.HTTP_200

    def __init__(self, db: Session):
        self.db = db
