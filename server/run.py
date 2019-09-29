from flask import Flask
from flask_restful import Resource, Api
from flask import Response, request
from server.keywords import RequestKeywordType, ResponseKeywordType, RequestEventDataType, RequestMethodDataType
from server.openvas_api.connector import OpenvasConnector
import server.openvas_api.jsonutils as json
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
        Returns a JSON style response with the parrent keys 'status' 
        and 'data'. 'data' has 'name' + 'id' as childs. 
        Expects a xml root element from the openvas connector. 
        """

        status = extract_status_from_xml(xml_root_element)
        data = extract_data_from_xml(xml_root_element)

        return {
            ResponseKeywordType.STATUS.value: status,
            ResponseKeywordType.DATA.value: data
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


class CredentialByName(GetRequestStrategy):
    def get(self, credential_name):
        self.setup()
        response = openvas.get_credentials(filter=credential_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class ReportFormats(GetRequestStrategy):
    def get(self):
        self.setup()
        self.api_response = openvas.get_report_formats()
        
        return self.return_response()


class ReportFormatByName(GetRequestStrategy):
    def get(self, report_format_name):
        self.setup()
        response = openvas.get_report_formats(report_format_name)
        xml_root = etree.fromstring(response)

        return self.make_json_response(xml_root)


class CreateAlert(PostRequestStrategy):
    def execute_api_call(self):
        name = json.get_name(self.request_body)
        method_data = {
            RequestMethodDataType.SEND_HOST.value : json.get_send_host(self.request_body),
            RequestMethodDataType.SEND_PORT.value : json.get_send_port(self.request_body),
            RequestMethodDataType.SEND_REPORT_FORMAT.value : json.get_send_report_format(self.request_body)
        }
        event_data = {
            RequestEventDataType.STATUS.value : json.get_status(self.request_body)
        }

        return openvas.create_xml_report_to_host_alert(name, method_data=method_data, event_data=event_data)


class CreateUsernamePasswortCredential(PostRequestStrategy):
    def execute_api_call(self):
        name = json.get_name(self.request_body)
        login = json.get_login(self.request_body)
        password = json.get_password(self.request_body)
        comment = json.get_comment(self.request_body)
        allow_insecure = json.get_allow_insecure(self.request_body)

        return openvas.create_username_password_credential(name, login, password, comment=comment, allow_insecure=allow_insecure)


class CreateTarget(PostRequestStrategy):
    def execute_api_call(self):
        name = json.get_name(self.request_body)
        make_unique = json.get_make_unique(self.request_body) 
        asset_hosts_filter = json.get_asset_hosts_filter(self.request_body) 
        hosts = json.get_hosts(self.request_body)
        comment = json.get_comment(self.request_body)
        exclude_hosts = json.get_exclude_hosts(self.request_body)
        ssh_credential_id = json.get_ssh_credential_id(self.request_body)
        ssh_credential_port = json.get_ssh_credential_port(self.request_body) 
        alive_test = json.get_alive_test(self.request_body) 
        reverse_lookup_only = json.get_reverse_lookup_only(self.request_body)
        reverse_lookup_unify = json.get_reverse_lookup_unify(self.request_body)
        port_range = json.get_port_range(self.request_body)
        port_list_id = json.get_port_list_id(self.request_body)

        return openvas.create_target(
            name,
            make_unique=make_unique,
            asset_hosts_filter=asset_hosts_filter,
            hosts=hosts,
            comment=comment,
            exclude_hosts=exclude_hosts,
            ssh_credential_id=ssh_credential_id,
            ssh_credential_port=ssh_credential_port,
            alive_test=alive_test,
            reverse_lookup_only=reverse_lookup_only,
            reverse_lookup_unify=reverse_lookup_unify,
            port_range=port_range,
            port_list_id=port_list_id
        )

    
class CreateTask(PostRequestStrategy):
    def execute_api_call(self):
        name = json.get_name(self.request_body)
        config_id = json.get_config_id(self.request_body)
        target_id = json.get_target_id(self.request_body)
        scanner_id = json.get_scanner_id(self.request_body)
        alert_ids = json.get_alert_ids(self.request_body)
        comment = json.get_comment(self.request_body)

        return openvas.create_task(name, config_id, target_id, scanner_id, alert_ids=alert_ids, comment=comment)


def extract_status_from_xml(xml_root_element):
    return xml_root_element.get(ResponseKeywordType.STATUS.value)

def extract_data_from_xml(xml_root_element):
    data = []

    for child in xml_root_element:
        elem = {}
        elem[ResponseKeywordType.NAME.value] = extract_name_from_xml(child)
        elem[ResponseKeywordType.ID.value] = extract_id_from_xml(child)

        # ensure that fields are populated
        if elem[ResponseKeywordType.NAME.value] and elem[ResponseKeywordType.ID.value]:
            data.append(elem)

    return data

def extract_id_from_xml(xml_element):
    return xml_element.get(ResponseKeywordType.ID.value)
        
def extract_name_from_xml(xml_element):
    name = None

    for child in xml_element:
        if child.tag == ResponseKeywordType.NAME.value:
            name = child.text
    
    return name


# GET routes
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
api.add_resource(CredentialByName, '/_credentials/<credential_name>')
api.add_resource(ReportFormats, '/_reportformats')
api.add_resource(ReportFormatByName, '/_reportformats/<report_format_name>')

# POST routes
api.add_resource(CreateAlert, '/_create/alert')
api.add_resource(CreateUsernamePasswortCredential, '/_create/username_password_credential')
api.add_resource(CreateTarget, '/_create/target')
api.add_resource(CreateTask, '/_create/task')

