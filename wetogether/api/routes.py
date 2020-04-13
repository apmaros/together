from falcon import API
from api.resources.statz import Statz
from api.resources.user_resource import UserResource



def set_routes(api: API, db) -> API:
    user=UserResource(db)
    api.add_route('/statz', Statz())
    api.add_route('/users/{user_id}', user)
    api.add_route('/users', user)
    return api
