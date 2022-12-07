from flask import Flask
from flask_restful import Api
from src.backend.controller.route import Route

app = Flask(__name__)
api = Api(app)

# Create www.example.com/{route, graph} logic
route = Route.Route()
graph = Route.Map()

# Tie endpoints to logic
api.add_resource(route, '/route')
api.add_resource(graph, '/graph')

if __name__ == '__main__':
    app.run()  # run Flask app