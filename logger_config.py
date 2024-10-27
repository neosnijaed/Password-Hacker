import os
from logging import getLogger, DEBUG, FileHandler, Formatter

LOG_FILE_NAME = 'hack.log'
LOG_FORMAT = '%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d %(message)s'


def create_new_log_file(log_file_name=LOG_FILE_NAME) -> None:
    """
    Create new log file if it does not exist.
    :param log_file_name: String containing the name of the log file to create if it does not exist.
    :return: None
    """
    if not os.path.exists(log_file_name):
        open(log_file_name, 'w').close()


def configure_logger(log_file_name=LOG_FILE_NAME, log_format=LOG_FORMAT) -> getLogger:
    """
    :param log_file_name: String containing the name of the log file where logs will be written.
    :param log_format: String containing the format in which the log messages will be written.
    :return: A configured logger instance with a file handler and specified format.
    """
    logg_inst = getLogger()
    logg_inst.setLevel(DEBUG)

    file_handler = FileHandler(log_file_name)
    create_new_log_file()

    formatter = Formatter(log_format)
    file_handler.setFormatter(formatter)

    logg_inst.addHandler(file_handler)
    return logg_inst


logger = configure_logger()
