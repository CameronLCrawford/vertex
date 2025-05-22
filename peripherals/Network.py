import socket
import time
from peripherals.Peripheral import Peripheral, Handler

BASE_ADDRESS = 0x400
MTU = 0x10

class Network(Peripheral):
    def __init__(self):
        super().__init__(0, (BASE_ADDRESS, BASE_ADDRESS + MTU))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 8080))
        with open("roms/network_handler", "rb") as program_file:
            program = bytearray(program_file.read())
            self.network_handler = Handler(BASE_ADDRESS + MTU, program)

    def init(self):
        for address in range(BASE_ADDRESS, BASE_ADDRESS + MTU):
            self.write(address, 0)

    def tick(self):
        packet, addr = self.sock.recvfrom(MTU)
        for i, byte in enumerate(packet):
            if i == MTU:
                break
            self.write(BASE_ADDRESS + i, byte)
        while not self.raise_(self.network_handler):
            time.sleep(0.01)
        time.sleep(0.01) # NOTE: there is a race between handler writing and this script reading to/from 0x401
        response = []
        for address in range(BASE_ADDRESS, BASE_ADDRESS + MTU):
            response.append(self.read(address))
        self.sock.sendto(bytearray(response), addr)

if __name__ == "__main__":
    network = Network()
    network.run()
