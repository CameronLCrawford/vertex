# Requirements

## ANTLR4
For general wisdom, see [here](https://tomassetti.me/antlr-mega-tutorial/).
For installation, install 4.13.2 from [here](https://www.antlr.org/download.html) and move the downloaded `.jar` to `/usr/local/lib/`.

## Python
- I currently use 3.13.3 but have also used 3.9.
- Requirements are in `requirements.txt`.
- Note that tkinter (used in the Display peripheral) doesn't come with Python via brew.

# Preparing to run a program
Executing a program on the CPU has three steps:
1. Building the VM to an executable
    - The VM is a single C file, `vertex.c`
    - `make` compiles to out/vertex with clang
2. Generating the control ROM
    - The CPU uses this to interpret instructions
    - `python generate_control.py -o roms/control`
3. Generate the program ROM
    - This is the instructions to be executed
    - Storn source --\[`compile_storn.py`\]-> vtx assembly --\[`assemble_vtx.py`\]-> program
    - To run `compile_storn.py` and `assemble_vtx.py`, you must generate the ANTLR4 parsers
    - `make storn-parser` and `make vtx-parser` will generate the respective parsers
    - `python compile_storn.py path/to/source.stn -o path/to/assembly.vtx` will generate the assembly for a given source file
    - `python assemble_vtx.py path/to/assembly.vtx -o roms/program` will generate the program ROM for a given assembly file
    - Note that you can pipe the output of the compiler into the assembler, ie. `python compile_storn.py path/to/source.stn | python assemble_vtx.py -o roms/program`
    - The assembler also supports stdout, ie. `python assemble_vtx.py path/to/assembly.vtx | xxd`

# Running a program
Once you've built everything, you can run the program with `./out/vertex roms/control roms/program`.
Note that the program writes to both stdout and stderr so a common pattern is `./out/vertex roms/control roms/program > out/log 2&>1`.
You can then execute subsequent programs by re-generating the program ROM (step 3., above).
