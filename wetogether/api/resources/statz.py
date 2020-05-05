import json
import os
import string

import falcon

def get_version() -> string:
    version = 'UNKNOWN'
    if 'BUILD_VERSION' in os.environ:
        version = os.environ['BUILD_VERSION']

    return version


class Statz(object):

    auth = {
        'exempt_methods': ['GET']
    }

    def on_get(self, _, resp):
        doc = {
            'version': get_version(),
        }

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
