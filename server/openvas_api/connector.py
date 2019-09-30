from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Gmp, CredentialType, AlertCondition, AlertEvent, AlertMethod
from lxml import etree
from gvm.transforms import EtreeCheckCommandTransform

class OpenvasConnector:
    """
    This class connects to the local openvasmd service via the specified socket
    and abstracts the api calls.
    """

    def __init__(self, socket_path='/var/run/openvasmd.sock', username='admin', password='admin'):
        self.username = username
        self.password = password
        connection = UnixSocketConnection(path=socket_path)
        transform = EtreeCheckCommandTransform()
        self.gmp = Gmp(connection=connection, transform=transform)

    def __authenticate__(self, gmp):
        gmp.authenticate(username=self.username, password=self.password)

    def get_version(self):
        with self.gmp as gmp:
            return etree.tostring(gmp.get_version(), pretty_print=True)

    def get_scanner(self, scanner_id):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_scanner(scanner_id))

    def get_scanners(self, filter=None, filter_id=None, trash=None, details=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_scanners(filter=filter, filter_id=filter_id, trash=trash, details=details))

    def get_configs(self, filter=None, filter_id=None, trash=None, details=None, families=None, preferences=None, tasks=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_configs(filter=filter, filter_id=filter_id, trash=trash, details=details, preferences=None, tasks=None))

    def get_targets(self, filter=None, filter_id=None, trash=None, tasks=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_targets(filter=filter, filter_id=filter_id, trash=trash, tasks=tasks))

    def get_tasks(self, filter=None, filter_id=None, trash=None, details=None, schedules_only=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_tasks(filter=filter, filter_id=filter_id, trash=trash, details=details, schedules_only=schedules_only))

    def get_alerts(self, filter=None, filter_id=None, trash=None, tasks=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_alerts(filter=filter, filter_id=filter_id, trash=trash, tasks=tasks))

    def get_report_formats(self, filter=None, filter_id=None, trash=None, alerts=None, params=None, details=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_report_formats(filter=filter, filter_id=filter_id, trash=trash, alerts=alerts, params=params, details=details))

    def get_port_lists(self, filter=None, filter_id=None, details=None, targets=None, trash=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_port_lists(filter=filter, filter_id=filter_id, details=details, targets=targets, trash=trash))

    def get_credentials(self, filter=None, filter_id=None, scanners=None, trash=None, targets=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_credentials(filter=filter, filter_id=filter_id, scanners=scanners, trash=trash, targets=targets))

    def create_credential(self, name, credential_type, comment=None, allow_insecure=None, certificate=None, key_phrase=None, private_key=None, 
                login=None, password=None,auth_algorithm=None, community=None, privacy_algorithm=None, privacy_password=None, public_key=None):
       
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.create_credential(
                name,
                credential_type,
                comment=comment,
                allow_insecure=allow_insecure,
                certificate=certificate,
                key_phrase=key_phrase,
                private_key=private_key, 
                login=login,
                password=password,
                auth_algorithm=auth_algorithm,
                community=community,
                privacy_algorithm=privacy_algorithm,
                privacy_password=privacy_password,
                public_key=public_key))

    def create_username_password_credential(self, name, login, password, comment=None, allow_insecure=None):
        """This method wraps the create_credentials method to provide an easy interface for username+password credential creation"""

        credential_type = CredentialType.USERNAME_PASSWORD
        return self.create_credential(name, credential_type, comment=comment, allow_insecure=allow_insecure, login=login, password=password)

    def create_target(self, name, make_unique=None, asset_hosts_filter=None, hosts=None, comment=None, exclude_hosts=None, 
            ssh_credential_id=None, ssh_credential_port=None, smb_credential_id=None, esxi_credential_id=None, snmp_credential_id=None, 
            alive_test=None, reverse_lookup_only=None, reverse_lookup_unify=None, port_range=None, port_list_id=None):
        
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.create_target(
                name, 
                make_unique=make_unique, 
                asset_hosts_filter=asset_hosts_filter, 
                hosts=hosts,
                comment=comment,
                exclude_hosts=exclude_hosts,
                ssh_credential_id=ssh_credential_id,
                ssh_credential_port=ssh_credential_port, 
                smb_credential_id=smb_credential_id,
                esxi_credential_id=esxi_credential_id,
                snmp_credential_id=snmp_credential_id,
                alive_test=alive_test, 
                reverse_lookup_only=reverse_lookup_only,
                reverse_lookup_unify=reverse_lookup_unify,
                port_range=port_range,
                port_list_id=port_list_id))

    def create_alert(self, name, condition, event, method, method_data=None, event_data=None, condition_data=None, filter_id=None, comment=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.create_alert(name, condition, event, method, method_data=method_data, event_data=event_data,
                condition_data=condition_data, filter_id=filter_id, comment=comment))

    def create_xml_report_to_host_alert(self, name, method_data=None, event_data=None, condition_data=None, filter_id=None, comment=None):
        condition = AlertCondition.ALWAYS
        event = AlertEvent.TASK_RUN_STATUS_CHANGED
        method = AlertMethod.SEND

        return self.create_alert(name, condition, event, method, method_data=method_data, event_data=event_data)

    def create_task(self, name, config_id, target_id, scanner_id, alterable=None, hosts_ordering=None, schedule_id=None, alert_ids=None,
            comment=None, schedule_periods=None, observers=None, preferences=None):

        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.create_task(
                name,
                config_id,
                target_id,
                scanner_id,
                alterable=alterable,
                hosts_ordering=hosts_ordering,
                schedule_id=schedule_id,
                alert_ids=alert_ids,
                comment=comment,
                schedule_periods=schedule_periods,
                observers=observers,
                preferences=preferences
            ))

    def start_task(self, task_id):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.start_task(task_id))

    def random_shit(self):
            print(self.gmp.authenticate('admin', 'admin'))
            root_node = gmp.get_scanners()

            # find all scanners
            scanners = root_node.findall('scanner')

            for scanner in scanners:
                print(etree.tostring(scanner, pretty_print=True))
                names = scanner.findall('name')

                for name in names:
                    print(name.text)

