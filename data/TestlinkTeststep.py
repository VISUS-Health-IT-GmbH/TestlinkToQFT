import util.TestlinkStringHelper as Helper

class TLTestStep:
    """
    Class that represents one Testlink-Teststep
    """
    def __init__(self, actions: list, expected_results: list, active: bool, execution_type: str):
        """
        Init method of Class TLTestStep
        :param actions: List of Strings that details how this Test Step is to be executed
        :param expected_results: List of Strings that details what results are to be expected
        :param active: boolean that denotes whether this test step is active or not
        :param execution_type: automatic or manual (or other) execution
        """
        # 1) "Actions"-String, cleaned
        self.actions = Helper.clean_html_entities(str(actions))

        # 2) "Expected-Results"-String, cleaned
        self.expected_results = Helper.clean_html_entities(str(expected_results))

        # 3) Other variables
        self.active = active
        self.execution_type = execution_type

