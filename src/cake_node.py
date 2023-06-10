import argparse
import socket
import re

import cake_utils as utils


class CakeNode:
    def __init__(self, address, debug=False):
        self.address = address
        self.debug = debug
        self.return_address = ""

    @staticmethod
    def __parse_udp_address(udp_address):
        pattern = r'^((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})|(localhost)):(\d{1,5})$'
        match = re.match(pattern, udp_address)

        if match:
            if match.group(2):
                ip_address = match.group(2)
            else:
                ip_address = '127.0.0.1'
            port_number = int(match.group(4))
            return ip_address, port_number
        else:
            return None

    @staticmethod
    def __string_to_bytes(s: str):
        return bytes(s, encoding="ascii")

    @staticmethod
    def __bytes_to_string(b: bytes):
        return b.decode(encoding="ascii")

    @staticmethod
    def __find_udp_address(cake: str) -> tuple:
        pattern = r"\b(?:localhost|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})):(\d{1,5});\b"
        match = re.search(pattern, cake)
        if match:
            address = match.group(1) or "localhost"
            port = int(match.group(2))
            rest = cake[match.end():]
            return (address, port, rest)
        else:
            return None

    def __peel_cake(self, cake: bytes) -> tuple:
        cake = self.__bytes_to_string(cake)
        self.return_ip, self.return_port, cake = self.__find_udp_address(
            cake)
        ip, port, cake = self.__find_udp_address(
            cake)
        cake = self.address + ';' + cake
        cake = self.__string_to_bytes(cake)
        return ip, port, cake

    @staticmethod
    def send_udp_message(ip, port, message_body):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(bytes(message_body, "ascii"), (ip, port))

    def send_further(self, cake):
        ip, port, cake = self.__peel_cake(cake)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        sock.sendto(cake, (ip, port))
        print("cake sent:", cake, "to", ip, port)

    def await_message(self) -> str:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.bind(self.__parse_udp_address(self.address))
        while True:
            data, addr = sock.recvfrom(1024)
            print("received message: %s" % data)
            print("peeled cake:", self.__peel_cake(data))
            return data

    def start(self):
        while True:
            cake = self.await_message()
            self.send_further(cake)
            response = self.await_message()
            self.send_message()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('address')
    # parser.add_argument('-d', '--debug',
    #                     action='debug_on')  # on/off flag
    args = parser.parse_args()

    cn = CakeNode(args.address, True)
    cn.start()
