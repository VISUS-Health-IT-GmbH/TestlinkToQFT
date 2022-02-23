# Importe aus Python-Bibiliotheken
import os
import json
import cherrypy
from cherrypy.lib.static import serve_file
import testlink.testlinkerrors
import requests

# Importe lokaler Dateien
from app import TestlinkConnection as Connection
from app import TestlinkFileWriter as FileWriter
from util import TestlinkLogger as Logger
from util import TestlinkStringHelper as Helper
from data import TestlinkTeststep as Teststep
from data import TestlinkTestcase as Testcase


@cherrypy.expose()
class TestlinkApplication:
    """
    Class containing http interfaces and general flow of execution
    """

    def __init__(self, config):
        """
        Init method of class Application
        :param config - TestlinkConfig Object containing configuration information
        """
        # 1) Config.JSON-Datei auslesen
        self.config = config

        # 2) Logger mit relativem Pfad zum log-Verzeichnis initialisieren
        self.logger = Logger.TestlinkLogger(
            os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "log", "Backend.log")))

    def read_library_names(self):
        """
        walks over library path specificed in config file

        :return: list of relative paths for all libraries
        """
        libraries = []

        # 1) Make request to Bitbucket API
        response = requests.get(
            "BITBUCKET API URL HERE").json()

        # 2) Filter items from response, save relative paths
        for item in response["values"]:
            if item.endswith(".qft") and "Libraries" in item:
                libraries.append(item.replace("Libraries/", ""))

        return libraries

    def build_testcase(self, response: dict, parameters: dict) -> Testcase:
        # 1) Variablen für Testfall-Objekt setzen
        # a) Format name = jx$ID_$name
        test_case_name = Helper.parse_tc_name(response)

        # 2) Testschritte auslesen und richtig hmtl-escaped als Liste von Objekten speichern
        teststeps = [Teststep.TLTestStep(
            item["actions"].encode('ascii', 'xmlcharrefreplace').decode('latin1'),
            item["expected_results"].encode('ascii', 'xmlcharrefreplace').decode('latin1'),
            item["active"],
            item["execution_type"])
            for item in response["steps"]]

        # 3) TLTestCase-Objekt initialisieren
        testcase = Testcase.TLTestCase(response["tc_external_id"],
                                       test_case_name,
                                       parameters["tc_version"],
                                       teststeps,
                                       response["summary"],
                                       self.config)
        return testcase

    def GET(self, request_type: str = None, testcase_id: str = None, testcase_version: int = None,
            includes: str = None):
        """
        get-Route the Frontend will make requests to

        :param request_type: string that specifies the requested functionality (see Readme)
        :param testcase_id: string, optional, testcase_id if testcase is requested
        :param testcase_version: integer, optional, testcase version if testcase is requested
        :param includes: string, optional, comma-separated list of libraries to be included
        :return: JSON-message containing status code and if any errors occured, their message
        """
        """0) GET-Requests can be made to /testcase/$ARGS or /library_names 
           thereforem, we have to differentiate here
           For a request for QF-Test Library-Names =>
           read library names from QF-Test Repository and return, otherwise continue """
        if request_type == "library_names":
            try:
                cherrypy.response.status = 200
                return json.dumps({"status": cherrypy.response.status,
                                   "message": self.read_library_names()})
            except Exception as e:
                self.logger.error(__file__, self.GET.__name__, "Could not get QFT-Libraries")
                cherrypy.response.status = 500
                return json.dumps({"status": cherrypy.response.status,
                                   "message": "Server-side Error: Could not get QFT-Libraries"})

        # 1) set TestcaseID and -Version
        #    TypeErrors and other possible input problems are handled in the frontend
        #    0 is the version fallback in case the user just wants to use the latest version
        #    in that case, we need to set version to None so that Testlink auto-returns the newest version
        if testcase_version in [0, "0"]:
            parameters = {"tc_id": testcase_id, "tc_version": None}
        else:
            parameters = {"tc_id": testcase_id, "tc_version": int(testcase_version)}

        tl_connector = Connection.TestlinkConnection(self.config, self.logger)

        # 2) Attempt connection and catch errors
        try:
            if not tl_connector.establish_connection():
                cherrypy.response.status = 500
                return json.dumps({"status": cherrypy.response.status,
                                   "message": "Connection to Testlink-Instance could not be established."})
        except testlink.testlinkerrors.TLConnectionError as e:
            self.logger.error(__file__, self.GET.__name__, "Could not establish connection"
                                                           f"to Testlink at {self.config.tl_api_url}" , str(e))

        # 3) If Connection was succesful:
        #    get a JSON response from Testlink and save to variable
        response = tl_connector.retrieve_test_case(parameters)

        # E) Check whether response contains an error key
        #   If yes: send to frontend and stop execution
        try:
            if response["error"] is not None:
                cherrypy.response.status = 404
                return json.dumps({"status": cherrypy.response.status,
                                   "message": response["error"]})
        except KeyError:
            # If no key "error" exists, we can continue
            pass

        # 4) Build testcase object
        testcase = self.build_testcase(response, parameters)

        # 4b) includes-list-string needs to be split around the commas
        includes = includes.split(",")

        # 5) Write Testcase from object
        xml_writer = FileWriter.FileWriter(testcase, includes, self.logger)

        # 5.1) get path to file from writing function
        file_path = xml_writer.write_file()

        cherrypy.response.status = 200

        # 6) Serve file with correct headers
        cherrypy.response.headers['content-type'] = 'application/xml;charset=ISO-8859-1'
        cherrypy.response.headers['name'] = testcase.qft_title + ".qft"
        cherrypy.response.headers['Content-Disposition'] = f'attachment; filename="{cherrypy.response.headers["name"]}"'

        return serve_file(file_path)
