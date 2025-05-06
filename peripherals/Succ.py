from peripherals.Peripheral import Handler, Peripheral
from assemble_vtx import assemble
import time

class Succ(Peripheral):
    def __init__(self):
        super().__init__(0, (500, 501))
        program = assemble("peripherals/succ.vtx")
        if not program:
            raise Exception("Assembler returned no program")
        self.succ_handler = Handler(501, program)

    def init(self):
        self.write(500, 0)

    def tick(self):
        while not self.raise_(self.succ_handler):
            time.sleep(0.001)

if __name__ == "__main__":
    succ = Succ()
    succ.run()
