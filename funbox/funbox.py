from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_redis import FlaskRedis

import json
import time
from functools import reduce
from urllib.parse import urlparse

app = Flask(__name__)
api = Api(app)
redis_client = FlaskRedis(app)


def decode_from_bin(data):
    return [ x.decode('utf-8') for x in data ]

def get_domain_from_url(url):
    if "//" in url:
        return urlparse(url).netloc.replace("www.","")
    else:
        return urlparse(f'//{url}').netloc.replace("www.", "")

def get_links_from_set(from_key, to_key):
    if None not in [from_key, to_key] and from_key <= to_key:
        sets = [redis_client.smembers(f'time:{key}:links') for key in range(from_key, to_key + 1)]
        return list(reduce(lambda x, y: x.union(y), sets))
    else:
        return []

#TODO: refactor
def put_links_in_set(_time, links):
    try:
        for key, link in enumerate(links):
            redis_client.sadd(f'time:{_time}:links', link)
        status = "ok"
    except Exception as error:
        status = repr(error)
    return status


class VisitedLinks(Resource):
    def post(self):
        links = request.json["links"]
        request_time = int(time.time())
        status = put_links_in_set(request_time, links)
        return {"status": f'{status}'}

class VisitedDomains(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('from', type=int, location="args")
        parser.add_argument('to', type=int, location="args")
        args = parser.parse_args()

        redis_data = get_links_from_set(args['from'], args['to'])
        try:
            if len(redis_data) != 0:
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

api.add_resource(VisitedLinks, '/visited_links')
api.add_resource(VisitedDomains, '/visited_domains')

if __name__ == '__main__':
    app.run()
