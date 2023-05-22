
import socket
import re


class CakeClient:
    def __init__(self, node_address_list: list, logging=False):
        self.node_address_list = node_address_list
        self.logging = logging

    def __construct_cake(self, message_body) -> str:
        cake_list = list(self.node_address_list[1:])
        cake_list.append(message_body)
        return ';'.join(cake_list)

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

    def __log_send_message(self, ip: str, port: int, message_body: str, cake: str) -> None:
        if (not self.logging):
            return
        log = "UDP target IP:" + ip + '\n'
        log += "UDP target port" + str(port) + '\n'
        log += "message:" + message_body + '\n'
        log += "cake:" + cake
        print(log)

    def send_message(self, message_body):
        cake = self.__construct_cake(message_body)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        ip, port = self.__parse_udp_address(self.node_address_list[0])
        sock.sendto(bytes(cake, "ascii"), (ip, port))
        self.__log_send_message(ip, port, message_body, cake)

    def await_message(self) -> str:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.bind(("localhost", 31337))
        while True:
            data, addr = sock.recvfrom(1024)
            print("received message: %s" % data)


cc = CakeClient(['192.168.132.40:31337'], logging=True)
cc.send_message('helo')
cc.await_message()
