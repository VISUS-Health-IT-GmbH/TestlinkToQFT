import os
from yattag import Doc
from yattag import indent

from data import TestlinkTestcase as Testcase
from util import TestlinkLogger as Logger


class FileWriter:
    """
    Class that takes a TLTestCase-Object and produces a .qft-xml file from it
    """
    def __init__(self, test_case: Testcase, includes: list, logger: Logger):
        """
        init Method of CLass FileWriter
        :param test_case: TestlinkTestCase to be written to file
        :param includes: list of qft libraries to be included
        """
        # 1) Instance variables
        self.test_case = test_case
        self.includes = includes
        self.logger = logger

        # 2) Set path to files folder
        if not os.path.exists(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..','files'))):
            os.mkdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', 'files')))
        file_location = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', 'files'))
        
        # 2) instantiate out_file
        self.out_file = open(file_location + "\\" + self.test_case.qft_title + ".qft", "w", encoding="ISO-8859-1")

    def write_file(self):
        """
        Writes an xml file using yattag

        :returns: full path of created file
        """

        # 1) Writer header
        self.out_file.write("<?xml version='1.0' encoding='ISO-8859-1'?> \n <!DOCTYPE RootStep>")

        # 2) initialize yattag objects
        doc, tag, text = Doc().tagtext()

        # 3) 1-indexed variable for Test-Steps
        stepindex = 1

        # 4) Write the file according to internal styleguide
        with tag("RootStep", id="_0", name="root", version="5.3.0"):
            for library in self.includes:
                with tag("include"):
                    text(library)
            with tag("comment"):
                text(f"{self.test_case.own_url}")
            with tag("TestSet", id="_1", name=self.test_case.qft_title):
                text()
                with tag("comment"):
                    text(self.test_case.summary)
                with tag("TestCase", id="_2", name=self.test_case.tl_external_id):
                    text()
                  # 4a) Teststeps are written here
                    for step in self.test_case.steps:
                        with tag("TestStep", name=f" Testschritt {stepindex}"):
                            stepindex += 1
                            with tag("comment"):
                                text(f"Aktionen = {step.actions} \n \n Erwartete Ergebnisse = {step.expected_results}")
            with tag("PackageRoot"):
                with tag("comment"):
                    text("Hier können Prozeduren abgelegt werden, die nur diesen Testfall betreffen")
            with tag("ExtraSequence"):
                with tag("comment"):
                    text("Dieser Bereich muss leerbleiben, nur für temporäre Aufnahmen zu verwenden!")
            with tag("WindowList"):
                with tag("comment"):
                    text("Auch dieser Bereich muss leer bleiben. "
                         "Fenster und Komponenten liegen immer in den oben eingebundenen, zentralen Bibliotheken!")

        # 5) write correctly indented content to file
        self.out_file.write(indent(doc.getvalue()))

        # 6) Close stream and log completion
        self.out_file.close()
        self.logger.info(__file__, self.write_file.__name__, f"Created file {self.out_file.name}")

        # 7) Finally, return the file location
        return self.out_file.name
