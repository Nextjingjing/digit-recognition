import tkinter as tk

from ui.Canvas import Canvas

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("200x250")
    canvas_widget = Canvas(root)
    canvas_widget.get_frame().pack(expand=True, fill=tk.BOTH)
    root.mainloop()