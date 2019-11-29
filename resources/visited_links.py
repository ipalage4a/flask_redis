from flask import request
from flask_restful import reqparse, Resource
import time
import validators


class VisitedLinks(Resource):
    def post(self):
        from models import put_links_in_set
        links = request.json["links"]
        validated_links = filter(
            lambda link: validators.url(link) == True, links)
        request_time = int(time.time())
        status = put_links_in_set(request_time, validated_links)
        return {"status": f'{status}'}
