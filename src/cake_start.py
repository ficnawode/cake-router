
import socket
import re

import cake_utils as utils


class CakeStart:
    def __init__(self, message: bytes, address: str, node_address_list: list, debug=True):
        self.message = message
        self.address = utils.parse_udp_address(address)
        self.node_address_list = node_address_list
        self.debug = debug

    def __construct_cake(self, message_body) -> bytes:
        cake_list = list(self.node_address_list[1:])
        cake_list.append(message_body)
        cake_list = [f'{self.address}', *cake_list]
        cake = ';'.join(cake_list)
        return utils.string_to_bytes(cake)

    def start(self):
        cake = self.__construct_cake(self.message)
        address = utils.parse_udp_address(self.node_address_list[0])
        utils.send_udp_message(address, cake)
        if self.debug:
            print("sent message:", cake, "to: ", address)
        response = utils.await_udp_message(self.address)
        if self.debug:
            print("received message: ", response)


if __name__ == '__main__':
    cc = CakeStart('helo', 'localhost:9000', ['localhost:9001', 'localhost:9002',
                                              'localhost:9003'], debug=True)
    cc.start()
