import unittest
import requests
import json


class BackendTest(unittest.TestCase):
    """
    This class contains tests for all routes offered by the backend
    requires the backend to be running and connected to a TestLink-Instance
    """
    def setUp(self) -> None:
        self.backend_url = "http://127.0.0.1:3110/tl2qft"

    def test_get_library_names_route(self):
        json_data = json.loads(requests.get(self.backend_url + "/library_names").text)
        assert(json_data["status"]) == 200
        assert(json_data["message"] is not None and type(json_data["message"]) is list)

    def test_get_testcase_route_correct_parameters(self):
        response = requests.get(self.backend_url + "/testcase/{testcase}/1/qfs.qft")
        assert(str(response) == "<Response [200]>")

    def test_get_testcase_route_incorrect_parameters(self):
        response = requests.get(self.backend_url + "/testcase/{this-testcase-doesnt-exist}/55/qfs.qft")
        assert(str(response) == "<Response [404]>")

    def test_get_testcase_route_malformed_parameters(self):
        response = requests.get(self.backend_url + "/testcase/this_should_be_status/five-hundred/qfs.qft")
        assert(str(response) == "<Response [500]>")


if __name__ == '__main__':
    unittest.main()