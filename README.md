# Instructions

## Compile CPU VM executable
`make`
**or**
`clang vertex.c -o out/vertex`

## Generate control ROM
`python3 generate_rom.py roms/control`

## Generate program ROM
`python3 generate_program.py roms/program`

## Run VM
`./out/vertex roms/control roms/program`

# Specification
A specification for the design and function of the CPU is given in `spec.md`.

