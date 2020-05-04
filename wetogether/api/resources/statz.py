import json
import falcon


class Statz(object):
    def on_get(self, _, resp):

        auth = {
            'exempt_methods': ['POST']
        }

        doc = {
            'version': "0.0.2",
        }

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
