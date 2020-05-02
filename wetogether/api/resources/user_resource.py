import json
import logging

import falcon

from api.security import encrypt
from model.user import User


class UserResource(object):
    logger = logging.getLogger(__name__)

    def on_get(self, req, resp, user_id=None):
        if user_id is None:
            resp.status = falcon.HTTP_400
            return

        resp.status = falcon.HTTP_200


    def on_post(self, req, resp):
        username = req.context.doc.get('username')
        email = req.context.doc.get('email')
        firstname = req.context.doc.get('firstname')
        lastname = req.context.doc.get('lastname')
        password_hash = encrypt(req.context.doc.get('password'))

        if username is None or email is None:
            resp.status = falcon.HTTP_400
            resp.body = json.dumps({'error': 'missing values'})
            resp.status = falcon.HTTP_401
            return

        user = User(
            username=username,
            email=email,
            first_name=firstname,
            last_name=lastname,
            password=password_hash
        )

        self.db.add(user)
        self.db.commit()
        resp.status = falcon.HTTP_200

    def __init__(self, db):
        self.db = db
