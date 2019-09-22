from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Gmp
from lxml import etree
from gvm.transforms import EtreeCheckCommandTransform

class OpenvasConnector:
    """
    This class connects to the local openvasmd service via the specified socket
    and abstracts the api calls.
    """

    def __init__(self):
        socket_path = '/var/run/openvasmd.sock'
        conn = UnixSocketConnection(path=socket_path)
        transform = EtreeCheckCommandTransform()
        self.gmp = Gmp(connection=conn, transform=transform)

    def __authenticate__(self):
        with self.gmp:
            self.gmp.authenticate(username='admin', password='admin')

    def get_version(self):
        with self.gmp:
            return etree.tostring(self.gmp.get_version(), pretty_print=True)

    def get_scanners(self):
        with self.gmp:
            self.gmp.authenticate(username='admin', password='admin')
            return etree.tostring(self.gmp.get_scanners())

    def get_scanner_by_name(self, scanner_name):
        with self.gmp:
            self.gmp.authenticate(username='admin', password='admin')
            return etree.tostring(self.gmp.get_scanners(filter=scanner_name))

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

