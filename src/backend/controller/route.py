from flask_restful import Resource, reqparse
from src.backend.model.map_model import MapModel
from src.backend.view.path_finding_view import PathFindingView
from flask import jsonify, request


class Route(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        parser = reqparse.RequestParser()

        parser.add_argument('orig', required=True)
        parser.add_argument('dest', required=True)
        parser.add_argument('max_min', required=True)
        parser.add_argument('variance', required=True)


        args = parser.parse_args()

        orig, dest, max_min, variance = args['orig'], args['dest'], args['max_min'], args['variance']

        map_model = MapModel("../../data/piedmont.graphml")
        path_finding_view = PathFindingView()

        route = path_finding_view.get_route(map_model.osm_network(), orig, dest, max_min, float(variance))

        print(route)

        response = jsonify(route)
        response.status_code = 200

        return response
