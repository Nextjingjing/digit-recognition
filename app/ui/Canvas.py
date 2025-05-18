import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

class Canvas:
    def __init__(self, root):
        self._frame = tk.Frame(root, bg="#cccccc")
        self._image = np.zeros((8, 8), dtype=np.uint8)
        self._create_ui()

    def get_image(self):
        return self._image

    def get_frame(self):
        return self._frame

    def _create_ui(self):
        self._canvas = tk.Canvas(self._frame, width=80, height=80, bg="white")
        self._canvas.pack()

        self._canvas.bind("<Button-1>", self._on_click)
        self._canvas.bind("<B1-Motion>", self._on_drag)

        btn_clear = tk.Button(self._frame, text="Clear", command=self._clear_canvas)
        btn_clear.pack(pady=10)

        btn_draw = tk.Button(self._frame, text="Predict", command=self.draw_image)
        btn_draw.pack(pady=5)

    def _on_click(self, event):
        self._last_x, self._last_y = event.x, event.y

    def _on_drag(self, event):
        x, y = event.x, event.y
        self._canvas.create_line(self._last_x, self._last_y, x, y, fill="black", width=8)
        self._canvas.create_oval(x-4, y-4, x+4, y+4, fill="black", outline="")
        self._last_x, self._last_y = x, y

    def _clear_canvas(self):
        self._canvas.delete("all")

    def _draw_line(self, img, x0, y0, x1, y1):
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)
        draw.line((x0, y0, x1, y1), fill=255, width=2)
        np.copyto(img, np.array(pil_img, dtype=np.uint8))

    def draw_image(self):
        img = np.zeros((80, 80), dtype=np.uint8)

        for item in self._canvas.find_all():
            coords = self._canvas.coords(item)
            if len(coords) >= 4:
                for i in range(0, len(coords) - 2, 2):
                    x0, y0 = int(coords[i]), int(coords[i + 1])
                    x1, y1 = int(coords[i + 2]), int(coords[i + 3])
                    self._draw_line(img, x0, y0, x1, y1)

        image8x8 = np.zeros((8, 8), dtype=np.uint8)
        for i in range(8):
            for j in range(8):
                block = img[i * 10:(i + 1) * 10, j * 10:(j + 1) * 10]
                avg_intensity = np.mean(block)
                image8x8[i, j] = int(avg_intensity / 255 * 15)

        self._image = image8x8

        self._canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x300")
    canvas_widget = Canvas(root)
    canvas_widget.get_frame().pack()
    root.mainloop()
