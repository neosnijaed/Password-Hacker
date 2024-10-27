import socket

from logger_config import logger


class SocketClient:
    """
    A client class for handling socket communications with a server.

    Attributes:
        host (str): The IP address of the server.
        port (int): The port number of the server.
        client_socket (socket.socket): The socket object for communication between the client and the server.
    """

    def __init__(self, host: str, port: int):
        """
        Initializes the SocketClient with the server's host and port.
        :param host: String containing the IP address of the server.
        :param port: Integer containing the port number of the server.
        """
        self.host = host
        self.port = port
        self.client_socket = socket.socket()

    def connect(self) -> None:
        """
        Establishes a connection to the server.

        Logs an error if the connection attempt fails, otherwise logs a successful connection.
        :return: None
        """
        try:
            self.client_socket.connect((self.host, self.port))
        except socket.error:
            logger.error(f'Client socket could not connect to server with address "{self.host}:{self.port}"')
        else:
            logger.info(f'Client socket connected to server with address "{self.host}:{self.port}"')

    def send_message(self, message: str) -> None:
        """
        Sends a message to the server.
        :param message: String containing the message to be sent to the server.
        :return: None
        """
        try:
            self.client_socket.send(message.encode())
        except socket.error:
            logger.error(f'Client socket could not send message "{message}" to server with address '
                         f'"{self.host}:{self.port}"')

    def receive_message(self, buffer_size: int = 1024) -> str:
        """
        Receives a message from the server.

        Logs an error and exits if the message could not be received.
        :param buffer_size: Integer containing the buffer size for receiving the message. Default is 1024.
        :return: String containing the received message from the server.
        """
        try:
            response = self.client_socket.recv(buffer_size)
        except socket.error:
            logger.error(f'Client socket could not receive message from server with address "{self.host}:{self.port}"')
            exit(1)
        else:
            return response.decode()

    def close(self) -> None:
        """
        Closes the connection to the server.

        Logs an error if the connection could not be closed, otherwise logs a successful closure.
        :return: None
        """
        try:
            self.client_socket.close()
        except socket.error:
            logger.error(
                f'Client socket could not close connection with server with address "{self.host}:{self.port}"')
        else:
            logger.info(f'Client socket closed connection with server with address "{self.host}:{self.port}"')
