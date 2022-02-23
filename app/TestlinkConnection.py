import testlink
import os

from app import TestlinkConfig
from util.TestlinkLogger import TestlinkLogger


class TestlinkConnection:
    """
    Class TestlinkConnection
    class that speaks to the Testlink Instance and retrieves data from it
    """
    def __init__(self, config: TestlinkConfig, logger: TestlinkLogger):
        """
        Constructor for class TestlinkConnection

        :param config: app-wide config reference
        :param logger: app-wide logger instance
        """

        # 1) Save config and logger instances
        self.config = config
        self.logger = logger

        # 2) Set environment variables for Testlink connection
        os.environ["TESTLINK_API_PYTHON_SERVER_URL"] = self.config.tl_api_url
        os.environ["TESTLINK_API_PYTHON_DEVKEY"] = self.config.dev_key

        # 3) Variable for TL connection, will be filled later
        self.connection = None

    def establish_connection(self):
        """
        Method that attempts to connect to the testlink instance
        returns: False if connection could not be established, True otherwise
        """
        try:
            self.connection = testlink.TestLinkHelper().connect(testlink.TestlinkAPIClient)
            self.logger.info(__file__, self.establish_connection.__name__, "- Connection to Testlink-System established")
            return True
        except testlink.testlinkerrors.TLConnectionError as e:
            return False

    def retrieve_test_case(self, parameters: dict) -> dict:
        """
        Queries Testlink API for a single testcase by ID and Version \n
        :param parameters: dict of {"tc_id": tc_id, "tc_version": tc_version}
        :return dict: response obtained from the TL server
        """
        try:
            # 1) Send a request to the testlink API
            # 1a) First parameter has to be None, placeholder for the internal id, which we dont know
            response = self.connection.getTestCase(
                None,
                testcaseexternalid=parameters["tc_id"],
                version=parameters["tc_version"])

            # E 1) If no TestCases with the chosen parameters are found, log error
        except testlink.testlinkerrors.TLResponseError as e:
            self.logger.error(__file__, self.retrieve_test_case.__name__,
                              "\n" + e.message + " ID and/or Version wrong, no matching testcases found \n")
            # E 2) and report
            return {"error": f" No testcase found for ID {parameters['tc_id']} | Version {parameters['tc_version']}"}

        # 2) return dictionary obtained from Testlink (item 0 in response list)
        return response[0]
