import falcon
from falcon import API
from api.resources.statz import Statz


def set_routes(api: API) -> API:
    api.add_route('/statz', Statz())
    return api
