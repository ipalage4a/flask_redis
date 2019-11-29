from flask import request
from flask_restful import reqparse, Resource
import time

class VisitedDomains(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=int, location="args")
        parser.add_argument('to', type=int, location="args")
        args = parser.parse_args()

        from models import get_links_from_set
        redis_data = get_links_from_set(args['from'], args['to'])
        try:
            if len(redis_data) != 0:
                from utils import decode_from_bin, get_domain_from_url
                domains = [get_domain_from_url(url) for url in decode_from_bin(redis_data) ]
                result = sorted(set(domains))
                status = 'ok'
            else:
                result = []
                status = 'No data!'
        except Exception as error:
            result = []
            status = repr(error)

        return {
                "domains": result,
                "status": status
                }
