import socket

class DetectorServer:

    def __init__(self, port, ip_address=socket.gethostbyname(), max_num_clients = 5):
        self._my_ip = ip_address
        self._my_port = port
        self._my_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._my_server_socket.bind((ip_address, 4000))
        self._max_clients = max_num_clients
        self._active_clients = {}

    def run(self):
        self._my_server_socket.listen(self._max_clients)