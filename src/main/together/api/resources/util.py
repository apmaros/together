import string


def get_param(req, param: string):
    return req.context.doc.get(param) \
        if param in req.context.doc else None
