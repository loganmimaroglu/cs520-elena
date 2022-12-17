from flask import Flask
from flask_restful import Api
from src.backend.controller.route import Route

app = Flask(__name__)
api = Api(app)


# Tie endpoints to logic
api.add_resource(Route, '/route')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
