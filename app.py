from flask import Flask, request
from flask_restful import Api
from flask_redis import FlaskRedis

app = Flask(__name__)
api = Api(app)
redis_client = FlaskRedis(app)

from resources.visited_domains import VisitedDomains
from resources.visited_links import VisitedLinks

api.add_resource(VisitedLinks, '/visited_links')
api.add_resource(VisitedDomains, '/visited_domains')

if __name__ == '__main__':
    app.run()

