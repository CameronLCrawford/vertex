import sys
import logging

def generate(rom_filename):
    # Control bits

    # Register in codes

    # Register out codes

    # ALU codes

    # Instructions
    # Each instruction is a list of control bit states.
    # Consider the contrived example in binary: [00, 11, 10].
    # This would define an instruction that is three microticks long
    # and would set the control bits to 00, 11, and 10, in turn.
    # To avoid writing binary, the variables defined above are used
    # to define instructions.
    # Consider the example of the ADDA instruction, which adds the
    # accumulator to itself:
    # ADDA := [A0 | ATI, ADD | AI].
    # Read as "1. A out, A Temp in; 2. Add, A in".
    # By taking the binary disjunction of control bits in each microtick,
    # complex control operations can be composed.
    # The `instructions` object is a list of all instructions
    instructions = [

    ]

    # Write out ROM
    rom_bytes = []
    with open(rom_filename, 'wb') as rom_file:
        rom_file.write(bytearray(rom_bytes))
    logging.info('Finished writing to ROM')

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) != 2:
        logging.error('Expected 1 argument')
    else:
        generate(arguments[1])

