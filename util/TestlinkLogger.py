import os
import datetime


class TestlinkLogger:
    """
    Simple logging functions
    """

    def __init__(self, log_path: str):
        """
        Constructor of class TestlinkLogger

        :param log_path: path to log file
        """

        if not os.path.exists(log_path):
            self.file = open(log_path, "w+")
        else:
            self.file = open(log_path, "a")

    def info(self, file: str, function: str, message: str):
        """
        Logs simple information with given parameters

        :param file: name of file where info(...) is used
        :param function: name of function where info(...) is used
        :param message: message to log
        """

        self.file.write(f"{datetime.datetime.now()} INFO: [{file}:{function}] {message}\n")
        self.file.flush()

    def warning(self, file: str, function: str, message: str, warning_message: str = None):
        """
        Logs warning with given parameters

        :param file: name of file where warning(...) is used
        :param function: name of function where warning(...) is used
        :param message: message to log
        :param warning_message: explicit warning message (from function etc.)
        """

        if warning_message:
            message = f"{datetime.datetime.now()} WARNING: [{file}:{function}] {message} - {warning_message}\n"
        else:
            message = f"{datetime.datetime.now()} WARNING: [{file}:{function}] {message}\n"

        self.file.write(message)
        self.file.flush()

    def error(self, file: str, function: str, message: str, error_message: str = None):
        """
        Logs error with given parameters

        :param file: name of file where warning(...) is used
        :param function: name of function where warning(...) is used
        :param message: message to log
        :param error_message: explicit error message (from exception etc.)
        """

        if error_message:
            message = f"{datetime.datetime.now()} ERROR: [{file}:{function}] {message} - {error_message}\n"
        else:
            message = f"{datetime.datetime.now()} ERROR: [{file}:{function}] {message}\n"

        self.file.write(message)
        self.file.flush()
