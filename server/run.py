from flask import Flask
from flask_restful import Resource, Api
from flask import Response, request
from server.openvas_api.connector import OpenvasConnector
import server.openvas_api.json as json
from lxml import etree

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
        self.json_response = "NOT IMPLEMENTED"

    def return_response(self):
        return Response(response=self.api_response, mimetype=self.mimetype)

    def make_json_response(self, xml_root_element):
        """
        Returns a JSON style response with the keys 'status', 'name' and 'id'. 
        Expects a xml root element from the openvas connector. 
        """
        id = extract_id_from_xml(xml_root_element)
        name = extract_name_from_xml(xml_root_element)
        status = extract_status_from_xml(xml_root_element)

        return {
            "status": status,
            "name": name,
            "id": id
        }
        

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
        response = openvas.get_scanners(filter=scanner_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)

    


class Configs(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_configs()

        return self.return_response() 


class ConfigByName(GetRequestStrategy):
    def get(self, config_name):
        self.setup()
        response = openvas.get_configs(filter=config_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class Targets(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_targets()

        return self.return_response() 


class TargetByName(GetRequestStrategy):
    def get(self, target_name):
        self.setup()
        response = openvas.get_targets(filter=target_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class Tasks(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_tasks()

        return self.return_response() 


class TaskByName(GetRequestStrategy):
    def get(self, task_name):
        self.setup()
        response = openvas.get_tasks(filter=task_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class Alerts(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_alerts()

        return self.return_response()


class AlertByName(GetRequestStrategy):
    def get(self, alert_name):
        self.setup()
        response = openvas.get_alerts(filter=alert_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class PortLists(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_port_lists()

        return self.return_response()


class PortListByName(GetRequestStrategy):
    def get(self, portlist_name):
        self.setup()
        response = openvas.get_port_lists(filter=portlist_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class Credentials(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_credentials()

        return self.return_response()


class CredentialsByName(GetRequestStrategy):
    def get(self, credentials_name):
        self.setup()
        response = openvas.get_port_lists(filter=credentials_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


def extract_status_from_xml(xml_root_element):
    return xml_root_element.get('status')

def extract_id_from_xml(xml_root_element):
        return xml_root_element[0].get('id')
        
def extract_name_from_xml(xml_root_element):
    name = None

    for child in xml_root_element[0]:
        if child.tag == 'name':
            name = child.text
    
    return name


api.add_resource(AliveTest, '/_alive')
api.add_resource(Scanners, '/_scanners')
api.add_resource(ScannerByName, '/_scanners/<scanner_name>')
api.add_resource(Configs, '/_configs')
api.add_resource(ConfigByName, '/_configs/<config_name>')
api.add_resource(Targets, '/_targets')
api.add_resource(TargetByName, '/_targets/<target_name>')
api.add_resource(Tasks, '/_tasks')
api.add_resource(TaskByName, '/_tasks/<task_name>')
api.add_resource(Alerts, '/_alerts')
api.add_resource(AlertByName, '/_alerts/<alert_name>')
api.add_resource(PortLists, '/_portlists')
api.add_resource(PortListByName, '/_portlists/<portlist_name>')
api.add_resource(Credentials, '/_credentials')
api.add_resource(CredentialsByName, '/_credentials/<credentials_name>')

