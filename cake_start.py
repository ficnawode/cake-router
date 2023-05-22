
import socket
import re


class CakeClient:
    def __init__(self, intermediate_addrs: list, destination_addr: str):
        # list of nodes on the way to the destination
        self.node_address_list = intermediate_addrs
        self.node_address_list.append(destination_addr)
        self.message = ''

    def __construct_cake(self, message_body) -> str:
        cake = ''
        for i in range(1, len(self.node_address_list)):
            cake += self.node_address_list[i] + ';'
        cake += message_body
        return cake

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

    def send_message(self, message_body):
        cake = self.__construct_cake(message_body)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        ip, port = self.__parse_udp_address(self.node_address_list[0])
        sock.sendto(bytes(cake, "ascii"), (ip, port))

        print("UDP target IP:", ip)
        print("UDP target port", port)
        print("message:", message_body)
        print("cake:", cake)

    def await_message(self) -> str:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.bind(("localhost", 31337))

        while True:
            data, addr = sock.recvfrom(1024)
            print("received message: %s" % data)


cc = CakeClient([], '192.168.132.40:31337')
cc.send_message('helo')
cc.await_message()
