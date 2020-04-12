import json
import falcon


class Statz(object):
    def on_get(self, _, resp):
        doc = {
            'version': "0.0.1",
        }

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
