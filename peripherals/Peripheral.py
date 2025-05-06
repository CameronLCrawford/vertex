from typing import Tuple
import ctypes
import abc
import os
import mmap
import time

RAM_SIZE = 65536
MAX_PERIPHERAL_COUNT = 8
RAM_SHM_FILENAME = "/tmp/vtx_ram_shm"
INTERRUPT_SHM_FILENAME = "/tmp/vtx_interrupt_shm"

class Handler:
    def __init__(self, address: int, program: bytearray):
        self.address = address

        ram_fd = os.open(RAM_SHM_FILENAME, os.O_RDWR)
        ram = mmap.mmap(ram_fd, RAM_SIZE)

        ram[address:address + len(program)] = program

class InterruptState(ctypes.Structure):
    _fields_ = [
        ("enabled", ctypes.c_uint8),
        ("_pad", ctypes.c_uint8),  # 1 byte padding for alignment
        ("handlerAddress", ctypes.c_uint16),
        ("raises", ctypes.c_uint8 * MAX_PERIPHERAL_COUNT),
    ]

class Peripheral(abc.ABC):
    def __init__(self, index: int, memory_range: Tuple[int, int]):
        self.index = index
        self.mem_start, self.mem_end = memory_range

        ram_fd = os.open(RAM_SHM_FILENAME, os.O_RDWR)
        self.ram = mmap.mmap(ram_fd, RAM_SIZE)

        interrupt_fd = os.open(INTERRUPT_SHM_FILENAME, os.O_RDWR)
        interrupt_state_mmap = mmap.mmap(interrupt_fd, ctypes.sizeof(InterruptState))
        self.interrupt_state = InterruptState.from_buffer(interrupt_state_mmap)

    def read(self, address):
        if address < self.mem_start or address >= self.mem_end:
            raise Exception(f"Peripheral {self.index} attempted to read from memory outside of its range")

        return self.ram[address]

    def write(self, address, value):
        if address < self.mem_start or address >= self.mem_end:
            raise Exception(f"Peripheral {self.index} attempted to write to memory outside of its range")

        self.ram[address] = value

    def raise_(self, handler: Handler):
        if not self.interrupt_state.enabled:
            return False

        self.interrupt_state.raises[self.index] = 1

        # Spin on acknowledgement
        while self.interrupt_state.raises[self.index]:
            time.sleep(0.01)

        self.interrupt_state.handlerAddress = handler.address
        self.interrupt_state.raises[self.index] = 1

        return True

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def tick(self):
        pass

    def run(self, tick_delay: float = 0.01):
        self.init()
        while True:
            self.tick()
            time.sleep(tick_delay)

