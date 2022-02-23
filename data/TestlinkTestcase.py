import util.TestlinkStringHelper as Helper
import app.TestlinkConfig as TestlinkConfig


class TLTestCase:
    """
    Class that represents an entire Testlink-Testcase
    """
    def __init__(self, tl_external_id: str, qft_title: str, version: int, steps: list, summary: str, tl_config: TestlinkConfig):
        """
        Init method of class TLTestCase
        :param tl_external_id: external id of test case
        :param qft_title: qft_title of the test case
        :param version: test case version
        :param steps: List of TLTestStep Objects that contain individual test steps
        :param summary: String containing summary of test contents
        :param tl_config: Configuration used across App
        """
        # 1) Instance variables
        self.tl_external_id = tl_external_id
        self.qft_title = qft_title
        self.version = version
        self.steps = steps

        # 1a) Summary variable, needs to be cleaned
        self.summary = summary
        self.summary = Helper.clean_html_entities(self.summary)

        # 1b) Config
        self.tl_config = tl_config

        # 2) Build url that links back to testlink webfrontend
        self.own_url = self.build_own_url()

    def build_own_url(self) -> str:
        """
        Method that puts together a link back to the Testlink-Testcase
        The response doesn't contain a link, but it is required per Styleguide
        returns: string that links back to testlink webgui for test in question
        """
        project_prefix = ""
        for index in range(len(self.qft_title)):
            if not self.qft_title[index].isnumeric():
                project_prefix += self.qft_title[index]
            else:
                break

        return Helper.clean_html_entities(f'<a target="_blank" href="{self.tl_config.tl_base_url}'
                                          f'/testlink/linkto.php?tprojectPrefix={project_prefix}'
                                          f'&item=testcase&id={project_prefix + "-" + self.tl_external_id}'
                                          f'"> Testlink Testcase {self.tl_external_id} </a>')


