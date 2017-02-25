# encoding : utf-8
import json

from flask import Response


class JSONResponse(Response):
    default_mimetype = 'application/json'

    def __init__(self, response=None, **kwargs):
        response = self.response_wrapper(response)
        super(JSONResponse, self).__init__(response, **kwargs)

    def response_wrapper(self, response):
        success = self.__class__.__dict__.get('success')
        res = dict()
        if success is True:
            res['success'] = True
            if response is not None:
                res['data'] = response
        else:
            res['success'] = False

        return json.dumps(res)


class SuccResponse(JSONResponse):
    success = True


class ErrResponse(JSONResponse):
    success = False
