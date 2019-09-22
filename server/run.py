from flask import Flask
from flask_restful import Resource, Api
from flask import Response
from server.openvas_api.connector import OpenvasConnector

app = Flask(__name__)
api = Api(app)

openvas = OpenvasConnector()

class AliveTest(Resource):
    def get(self):
        api_response = openvas.get_version()

        res = Response(response=api_response, mimetype='application/xml')
        # res.headers['Content-Type'] = "text/xml; charset=utf-8"
        return res


class Scanners(Resource):
    def get(self):
        api_response = openvas.get_scanners()

        res = Response(response=api_response, mimetype='application/xml')
        # res.headers['Content-Type'] = "text/xml; charset=utf-8"
        return res

class ScannerByName(Resource):
    def get(self, scanner_name):
        api_response = openvas.get_scanner_by_name(scanner_name)

        res = Response(response=api_response, mimetype='application/xml')
        return res

api.add_resource(AliveTest, '/_alive')
api.add_resource(Scanners, '/_scanners')
api.add_resource(ScannerByName, '/_scanners/name/<scanner_name>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')