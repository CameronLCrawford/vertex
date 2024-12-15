import sys
import logging

def generate_program(rom_filename):
    rom_bytes = [0] * 65536
    # Program that calculates and outputs power of 2
    # Halts at zero
    # setup: LDA 1
    # main loop: OUT, SHLA
    # maybe end: JZI end
    # jump: JI main loop
    # end: HLT
    # [LDA, 1, OUT, SHLA, JZI, 128, 10, JMPI, 128, 2, HLT]
    program = [2, 1, 5, 1, 3, 128, 10, 4, 128, 2, 6]
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

