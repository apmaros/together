from sqlalchemy.orm import Session
from falcon_auth import JWTAuthBackend
from config.jwt_config import JwtConfig
from model.user import User


class JwtAuth(object):
    def get_backend(self) -> JWTAuthBackend:
        return JWTAuthBackend(
            user_loader=self.__get_user(),
            secret_key=self.config.secret,
            algorithm=self.config.algorithm,
            required_claims=['exp']
        )


    def __get_user(self):
        return lambda token: {
            self.db.query(User).filter(User.id == token['user_id']).one()
        }

    def __init__(self, config: JwtConfig, db: Session):
        print(config)
        self.db = db
        self.config = config
