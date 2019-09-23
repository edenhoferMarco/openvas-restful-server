from flask import Flask
from flask_restful import Resource, Api
from flask import Response, request
from server.openvas_api.connector import OpenvasConnector

app = Flask(__name__)
api = Api(app)

openvas = OpenvasConnector()

class GetRequestTemplate(Resource):
    """
    This is a implementation of the Template Method Design Pattern.
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


class AliveTest(GetRequestTemplate):
    def execute_api_call(self):
        return openvas.get_version()


class Scanners(GetRequestTemplate):
    def execute_api_call(self):
        filter = get_filter_from_json(self.request_body)
        filter_id = get_filter_id_from_json(self.request_body)
        trash = get_trash_from_json(self.request_body)
        details = get_details_from_json(self.request_body)

        return openvas.get_scanners(filter=filter, filter_id=filter_id, trash=trash, details=details)


class ScannerById(GetRequestTemplate):
    def execute_api_call(self):
        scanner_id = get_scanner_id_from_json(self.request_body)

        return openvas.get_scanner(scanner_id)


api.add_resource(AliveTest, '/_alive')
api.add_resource(ScannerById, '/_scanner/id')
api.add_resource(Scanners, '/_scanners')

def get_filter_from_json(json_data):
    name = json_data.get('filter')

    if name != None and len(name) > 0:
        return name
    else:
        return None

def get_filter_id_from_json(json_data):
    filter_id = json_data.get('filter_id')

    if filter_id != None and len(filter_id) > 0:
        return filter_id
    else:
        return None

def get_trash_from_json(json_data):
    trash = json_data.get('trash')

    if trash != None and (trash == 'True' or trash == 'False'):
        return trash
    else:
        return None

def get_details_from_json(json_data):
    details = json_data.get('details')

    if details != None and (details == 'True' or details == 'False'):
        return details
    else:
        return None

def get_scanner_id_from_json(json_data):
    scanner_id = json_data.get('scanner_id')

    if scanner_id != None and len(scanner_id) > 0:
        return scanner_id
    else:
        return None