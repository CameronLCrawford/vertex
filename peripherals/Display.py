import tkinter as tk
from peripherals.Peripheral import Peripheral

BASE_ADDRESS = 8192
SCALE = 16
ROWS = 32
COLS = 32
FPS = 30

class Display(Peripheral):
    def __init__(self):
        super().__init__(1, (BASE_ADDRESS, BASE_ADDRESS + ROWS * COLS // 8))
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=COLS * SCALE, height=ROWS * SCALE, bg="black")
        self.canvas.pack()
        self.pixels = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for y in range(ROWS):
            for x in range(COLS):
                self.pixels[y][x] = self.canvas.create_rectangle(
                    x * SCALE, y * SCALE, (x + 1) * SCALE, (y + 1) * SCALE,
                    outline="", fill="black"
                )

    def init(self):
        pass

    def tick(self):
        for y in range(ROWS):
            row_base = self.mem_start + (y * (COLS // 8))
            for x_byte in range(COLS // 8):
                byte = self.read(row_base + x_byte)
                for bit in range(8):
                    x = x_byte * 8 + bit
                    pixel_state = (byte >> (7 - bit)) & 1
                    color = "lawn green" if pixel_state else "black" # looks "retro"
                    self.canvas.itemconfig(self.pixels[y][x], fill=color)
        self.root.update()

if __name__ == "__main__":
    display = Display()
    display.run(1/FPS)
