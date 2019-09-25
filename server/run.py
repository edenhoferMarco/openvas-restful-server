from flask import Flask
from flask_restful import Resource, Api
from flask import Response, request
from server.openvas_api.connector import OpenvasConnector

import server.openvas_api.json as json

app = Flask(__name__)
api = Api(app)

openvas = OpenvasConnector()

class GetRequestStrategy(Resource):
    """
    This is a implementation of the Strategy Design Pattern.
    This class provides a basic execution sequence, usually the extending class only needs to implement the function execute_api_call().
    """ 

    def setup(self):
        self.request_body = request.get_json()
        self.mimetype = 'application/xml'
        self.api_response = "NOT IMPLEMENTED"

    def execute_api_call(self):
        pass

    def return_response(self):
        return Response(response=self.api_response, mimetype=self.mimetype)

    def get(self):
        self.setup()
        self.api_response = self.execute_api_call()
        return self.return_response()


class AliveTest(GetRequestStrategy):
    def execute_api_call(self):
        return openvas.get_version()


class Scanners(GetRequestStrategy):
    def execute_api_call(self):
        filter = json.get_filter(self.request_body)
        filter_id = json.get_filter_id(self.request_body)
        trash = json.get_trash(self.request_body)
        details = json.get_details(self.request_body)

        return openvas.get_scanners(filter=filter, filter_id=filter_id, trash=trash, details=details)


class ScannerById(GetRequestStrategy):
    def execute_api_call(self):
        scanner_id = json.get_scanner_id(self.request_body)

        return openvas.get_scanner(scanner_id)


api.add_resource(AliveTest, '/_alive')
api.add_resource(ScannerById, '/_scanner/id')
api.add_resource(Scanners, '/_scanners')

