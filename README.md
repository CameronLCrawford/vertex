# Requirements

## antlr4
For general wisdom, see [here](https://tomassetti.me/antlr-mega-tutorial/).
For installation, install 4.13.2 from [here](https://www.antlr.org/download.html) and move the downloaded `.jar` to `/usr/local/lib/`.

## Python
- I currently use 3.13.3 but have also used 3.9.
- Requirements are in `requirements.txt`.
- Note that tkinter (used in the Display peripheral) doesn't come with Python via brew.

## roms directory
`mkdir roms`

# Operations

## Compile CPU VM executable
`make`
**or**
`clang vertex.c -o out/vertex`

## Generate ANTLR outputs
`make storn-parser`
**and**
`make vtx-parser`

## Generate control ROM
`python generate_control.py roms/control`

## Assemble program
`python assemble_vtx.py path/to/program.vtx roms/program`

## Run VM
`./out/vertex roms/control roms/program`
**or**
`./out/vertex roms/control roms/program > out/log 2>&1`

