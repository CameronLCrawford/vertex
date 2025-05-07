import tkinter as tk
from peripherals.Peripheral import Peripheral

FPS = 60
SCALE = 3

class Display(Peripheral):
    def __init__(self):
        super().__init__(1, (8192, 16384))
        self.width = 256
        self.height = 256
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.width * SCALE, height=self.height * SCALE, bg="black")
        self.canvas.pack()
        self.pixels = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self.pixels[y][x] = self.canvas.create_rectangle(
                    x * SCALE, y * SCALE, (x + 1) * SCALE, (y + 1) * SCALE,
                    outline="", fill="white"
                )

    def init(self):
        for i in range(8192, 16384):
            self.write(i, 0)

    def tick(self):
        for y in range(self.height):
            row_base = self.mem_start + (y * (self.width // 8))
            for x_byte in range(self.width // 8):
                byte = self.read(row_base + x_byte)
                for bit in range(8):
                    x = x_byte * 8 + bit
                    pixel_state = (byte >> (7 - bit)) & 1
                    color = "black" if pixel_state else "white"
                    self.canvas.itemconfig(self.pixels[y][x], fill=color)
        self.root.update()

if __name__ == "__main__":
    display = Display()
    display.run(1/FPS)
