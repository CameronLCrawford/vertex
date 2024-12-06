import sys
import logging

def generate_program(rom_filename):
    rom_bytes = [0] * 65536
    # Program that calculates and outputs power of 2
    # setup: LDA 1
    # main loop: OUT, SHLA
    # jump: JMPI main loop
    # [LDA, 1, OUT, SHLA, JMPI, 128, 2]
    program = [2, 1, 4, 1, 3, 128, 2]
    rom_address = 32768
    for instruction in program:
        rom_bytes[rom_address] = instruction
        rom_address += 1
    with open(rom_filename, 'wb') as rom_file:
        rom_file.write(bytearray(rom_bytes))

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 2:
        logging.error('Expected 1 argument')
    else:
        generate_program(arguments[1])

