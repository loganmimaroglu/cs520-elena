from flask_restful import Resource, reqparse

class Map(Resource):

    def get(self):
        parser = reqparse.RequestParser()

        parser.add_argument('orig', required=True)
        parser.add_argument('dest', required=True)
        parser.add_argument('max_min', required=False)
        parser.add_argument('variance', required=False)

        args = parser.parse_args()

        print(args)

        return {'data': 'hi'}, 200