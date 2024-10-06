# Instructions

## Compile CPU VM executable
`clang vertex.c -o out/vertex`

## Generate control ROM
`python3 generate_rom.py roms/control`

## Generate program ROM
TODO

## Run VM
`./out/vertex roms/control roms/program`

# Specification
A specification for the design and function of the CPU is given in `spec.md`.

# History
A brief narrative of the history of this project is given in `narrative.md`.

