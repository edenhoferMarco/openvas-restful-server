from flask import Flask
from flask_restful import Resource, Api
from flask import Response, request
from server.openvas_api.connector import OpenvasConnector
import server.openvas_api.json as json

app = Flask(__name__)
api = Api(app)

openvas = OpenvasConnector()


class PostRequestStrategy(Resource):
    """
    This is an implementation of the Strategy Design Pattern.
    This class provides a basic execution sequence (setup and return_response) for POST requests, 
    usually the extending class only needs to implement the function execute_api_call().
    """ 

    def setup(self):
        self.request_body = request.get_json()
        self.mimetype = 'application/xml'
        self.api_response = "NOT IMPLEMENTED"

    def execute_api_call(self):
        """
        The specific execution sequence shall be implemented in this method. 
        Shall return the desired response, provided by the REST Api.
        """
        pass

    def return_response(self):
        return Response(response=self.api_response, mimetype=self.mimetype)

    def post(self):
        self.setup()
        self.api_response = self.execute_api_call()
        return self.return_response()


class GetRequestStrategy(Resource):
    """
    This is an implementation of the Strategy Design Pattern.
    This class provides a basic execution sequence (setup and return_response) for GET requests, 
    usually the extending class only needs to implement the function get() and may fill it with existing methods.
    """ 

    def setup(self):
        self.mimetype = 'application/xml'
        self.api_response = "NOT IMPLEMENTED"

    def return_response(self):
        return Response(response=self.api_response, mimetype=self.mimetype)

    def get(self):
        """
        The specific execution sequence and input parameters shall be implemented in this method. 
        Shall return the desired response, provided by the REST Api.
        """
        self.api_response = self.execute_api_call()
        return self.return_response()


class AliveTest(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_version()
        return self.return_response()


class Scanners(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_scanners()

        return self.return_response()

class ScannerByName(GetRequestStrategy):
    def get(self, scanner_name):
        self.setup()
        self.api_response = openvas.get_scanners(filter=scanner_name)

        return self.return_response()


class Configs(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_configs()

        return self.return_response() 


class ConfigByName(GetRequestStrategy):
    def get(self, config_name):
        self.setup()
        self.api_response = openvas.get_configs(filter=config_name)

        return self.return_response() 


class Targets(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_targets()

        return self.return_response() 


class TargetByName(GetRequestStrategy):
    def get(self, target_name):
        self.setup()
        self.api_response = openvas.get_targets(filter=target_name)

        return self.return_response() 


api.add_resource(AliveTest, '/_alive')
api.add_resource(Scanners, '/_scanners')
api.add_resource(ScannerByName, '/_scanners/<scanner_name>')
api.add_resource(Configs, '/_configs')
api.add_resource(ConfigByName, '/_configs/<config_name>')
api.add_resource(Targets, '/_targets')
api.add_resource(TargetByName, '/_targets/<target_id>')

