import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw
import joblib
import os

class Canvas:
    def __init__(self, root):
        self._frame = tk.Frame(root, bg="#cccccc", bd=3, relief="ridge")
        self._image = np.zeros((8, 8), dtype=np.uint8)
        self._create_ui()
        self._load_model()
        

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

        btn_draw = tk.Button(self._frame, text="Predict", command=self._predict)
        btn_draw.pack(pady=5)

        self._pred_var = tk.StringVar()
        self._pred_var.set("Predict: Null")

        pred_label = tk.Label(self._frame, textvariable=self._pred_var)
        pred_label.pack()

    def _on_click(self, event):
        self._last_x, self._last_y = event.x, event.y

    def _on_drag(self, event):
        x, y = event.x, event.y
        self._canvas.create_line(self._last_x, self._last_y, x, y, fill="black", width=8)
        self._canvas.create_oval(x-4, y-4, x+4, y+4, fill="black", outline="")
        self._last_x, self._last_y = x, y

    def _clear_canvas(self):
        self._canvas.delete("all")
        self._pred_var.set("Predict: Null")

    def _draw_line(self, img, x0, y0, x1, y1):
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)
        draw.line((x0, y0, x1, y1), fill=255, width=2)
        np.copyto(img, np.array(pil_img, dtype=np.uint8))

    def _predict(self):
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
        pred = self._model.predict(self._image.reshape(1, -1))[0]
        self._pred_var.set(f"Predict: {pred}")

    def _load_model(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "..", "model", "digit_recognizer_model.pkl")
        self._model = joblib.load(model_path)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("175x200")
    canvas_widget = Canvas(root)
    canvas_widget.get_frame().pack()
    root.mainloop()
