from falcon import API
from sqlalchemy.orm import Session

from api.resources.login_resource import LoginResource
from api.resources.statz import Statz
from api.resources.user_resource import UserResource



def set_routes(api: API, db: Session) -> API:
    user = UserResource(db)
    api.add_route('/statz', Statz())
    api.add_route('/users/{user_id}', user)
    api.add_route('/users', user)
    api.add_route('/login', LoginResource(db))
    return api
