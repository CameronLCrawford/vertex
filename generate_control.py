import sys
import logging
from instructions import instructions, invalid_conditional_jump

def generate_control(rom_filename):
    # The control ROM is addressed using the following composition of bits:
    # CF|SF|ZF|I7|I6|I5|I4|I3|I2|I1|I0|M3|M2|M1|M0
    # 14 13 12 11 10 09 08 07 06 05 04 03 02 01 00
    # The first 3 are flag bits (carry, sign, zero).
    # The next 8 are the current instruction index.
    # The final 4 are the microinstruction index.
    # Most instructions aren't influenced by the current flag states.
    # These instructions are duplicated 2**3=8 (3 flags) times across the ROM.
    # Some instructions depend on specific flag states.
    # These instructions are only duplicated where these conditions are met.
    rom = [0] * 65536
    for flag_state in range(8):
        for i, instruction in enumerate(instructions):
            # TODO: document handling of scopes
            scopes = instruction[3]
            valid_flag = True
            for flag in range(3):
                if scopes[flag] == 1 and not ((flag_state >> flag) & 1):
                    valid_flag = False
                if scopes[flag] == -1 and ((flag_state >> flag) & 1):
                    valid_flag = False
            if valid_flag:
                microinstructions = instruction[2]
            else:
                microinstructions = invalid_conditional_jump
            for j, microinstruction in enumerate(microinstructions):
                address = (flag_state << 12) | (i << 4) | j
                rom[address] = microinstruction

    # Write out ROM
    rom_bytes = []
    for value in rom:
        value = bin(value)[2:].zfill(32)
        rom_bytes.append(int(value[24:32], 2))
        rom_bytes.append(int(value[16:24], 2))
        rom_bytes.append(int(value[8:16], 2))
        rom_bytes.append(int(value[:8], 2))
    with open(rom_filename, 'wb') as rom_file:
        rom_file.write(bytearray(rom_bytes))
    logging.info('Finished writing to ROM')

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 2:
        logging.error('Expected 1 argument')
    else:
        generate_control(arguments[1])

