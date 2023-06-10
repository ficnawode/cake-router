import argparse
import socket
import re
from typing import Tuple

import cake_utils as utils
from udp_address import UDPAddress


class CakeNode:
    def __init__(self, address: str, debug=False):
        self.address = utils.parse_udp_address(address)
        self.debug = debug
        self.return_address = ('', 0)

    def __peel_cake(self, cake: bytes) -> Tuple[UDPAddress, bytes]:
        cake = utils.bytes_to_string(cake)
        self.return_address, cake = utils.find_udp_address(
            cake)
        next_address, cake = utils.find_udp_address(
            cake)
        cake = f'{self.address};' + cake
        cake = utils.string_to_bytes(cake)
        return next_address, cake

    def send_further(self, cake):
        address, cake = self.__peel_cake(cake)
        utils.send_udp_message(address, cake)
        if self.debug:
            print("cake sent:", cake, "to", address)

    def start(self):
        cake = utils.await_udp_message(self.address)
        self.send_further(cake)
        response = utils.await_udp_message(self.address)
        utils.send_udp_message(self.return_address, response)


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
