import tkinter as tk
from typing import Callable

from PIL import Image, ImageTk

from browsed_image import BrowsedImage
from consts import IMAGE_CONTAINER_HEIGHT, IMAGE_CONTAINER_WIDTH
from utils import get_scaled_size


# not in use
def init_image(root: tk.Tk, image_path: str) -> tk.Label:
    pilimg = Image.open(image_path)
    if pilimg.mode != "RGB":
        pilimg = pilimg.convert("RGB")
    old_width, old_height = pilimg.width, pilimg.height
    new_width, new_height = get_scaled_size(old_width, old_height, 1422, 800)
    pilimg = pilimg.resize((new_width, new_height))
    img = ImageTk.PhotoImage(pilimg)
    label = tk.Label(root, image=img)  # type: ignore
    label.pack()
    return label


def add_button(root: tk.Frame, text: str, column: int, callback: Callable) -> tk.Button:
    btn = tk.Button(
        root,
        text=text,
        font=("Arial", 14, "bold"),
        bg="#0e0e0e",
        fg="white",
        activebackground="black",
        activeforeground="white",
        padx=20,
        pady=10,
        command=callback,
    )

    btn.grid(row=0, column=column, padx=10, pady=5)
    return btn


def init_root(width: int, height: int) -> tk.Tk:
    root = tk.Tk()
    root.geometry(f"{width}x{height}")
    root.configure(bg="black")
    root.title("Image browser")
    return root


def change_image(label: tk.Label, image_path: str) -> tk.Label:
    pilimg = Image.open(image_path)
    if pilimg.mode != "RGB":
        pilimg = pilimg.convert("RGB")
    old_width, old_height = pilimg.width, pilimg.height
    new_width, new_height = get_scaled_size(
        old_width, old_height, IMAGE_CONTAINER_WIDTH, IMAGE_CONTAINER_HEIGHT
    )
    pilimg = pilimg.resize((new_width, new_height))
    img = ImageTk.PhotoImage(pilimg)
    label.configure(image=img)  # type: ignore
    label.image = img  # type: ignore
    return label
