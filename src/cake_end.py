import argparse

import cake_utils as utils
from typing import Tuple
from udp_address import UDPAddress


class CakeEnd:
    def __init__(self, address: str, debug=False):
        self.address = utils.parse_udp_address(address)
        self.debug = debug

    def __peel_cake(self, cake: bytes) -> str:
        cake = utils.bytes_to_string(cake)
        self.return_address, message = utils.find_udp_address(
            cake)
        return message

    def start(self) -> str:
        cake = utils.await_udp_message(self.address)
        message = self.__peel_cake(cake)
        utils.send_udp_message(self.return_address, b'ACK')
        if self.debug:
            print("Message acquired: ", message)
        return message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('address')
    # parser.add_argument('-d', '--debug',
    #                     action='debug_on')  # on/off flag
    args = parser.parse_args()

    cn = CakeEnd(args.address, True)
    cn.start()
