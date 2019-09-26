from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Gmp
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

    def get_port_lists(self, filter=None, filter_id=None, details=None, targets=None, trash=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_port_lists(filter=filter, filter_id=filter_id, details=details, targets=targets, trash=trash))

    def get_credentials(self, filter=None, filter_id=None, scanners=None, trash=None, targets=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_credentials(filter=filter, filter_id=filter_id, scanners=scanners, trash=trash, targets=targets))



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

