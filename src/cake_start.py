
import socket
import re


class CakeStart:
    def __init__(self, message: str, address: str, node_address_list: list, debug=False):
        self.message = message
        self.address = address
        self.node_address_list = node_address_list
        self.debug = debug

    def __construct_cake(self, message_body) -> str:
        cake_list = list(self.node_address_list[1:])
        cake_list.append(message_body)
        cake_list = [self.address, *cake_list]
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

    def send_message(self, message_body):
        cake = self.__construct_cake(message_body)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
        ip, port = self.__parse_udp_address(self.node_address_list[0])
        sock.sendto(bytes(cake, "ascii"), (ip, port))
        if self.debug:
            print("sent message:", cake, "to: ", ip, port)

    def await_message(self) -> str:
        sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)
        sock.bind(self.__parse_udp_address(self.address))
        data, addr = sock.recvfrom(1024)
        print("received message: %s" % data)


if __name__ == '__main__':
    cc = CakeStart('helo', 'localhost:9000', ['localhost:9001', 'localhost:9002',
                                              'localhost:9003'], debug=True)
    cc.send_message('helo')
    cc.await_message()
