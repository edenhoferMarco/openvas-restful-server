from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Gmp
from lxml import etree
from gvm.transforms import EtreeCheckCommandTransform

class OpenvasConnector:
    """
    This class connects to the local openvasmd service via the specified socket
    and abstracts the api calls.
    """

    def __init__(self, *, socket_path='/var/run/openvasmd.sock', username='admin', password='admin'):
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

    def get_scanners(self, *, filter=None, filter_id=None, trash=None, details=None):
        with self.gmp as gmp:
            self.__authenticate__(gmp)
            return etree.tostring(gmp.get_scanners(filter=filter, filter_id=filter_id, trash=trash, details=details))


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

