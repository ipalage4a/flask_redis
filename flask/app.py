from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_redis import FlaskRedis
import json

app = Flask(__name__)
api = Api(app)
redis_client = FlaskRedis(app)

# parser = reqparse.RequestParser()
# parser.add_argument('links', type=list, required=True, help="Must be LINKS", location='json')
def decode_from_bin(data):
    return [ x.decode('utf-8') for x in data ]


class Home(Resource):
    def get(self):
        redis_data = redis_client.lrange("links", 0, -1)
        return {"links": decode_from_bin(redis_data)}
    def post(self):
        links = request.json["links"]
        try:
            redis_client.rpush("links", *links )
            status = "ok"
        except Exception as error:
            status = repr(error)

        return {"status": f'{status}'}




class VisitedLinks(Resource):
    def post(self):
        return {'hello': 'world'}

class VisitedDomains(Resource):
    def get(self):
        return links

api.add_resource(Home, '/')
# api.add_resource(VisitedLinks, '/visited_links')
# api.add_resource(VisitedDomains, '/visited_domains')

if __name__ == '__main__':
    app.run(debug=True)
