import sys
import tkinter as tk

from browsed_image import ImageManager
from tkinter_funcs import change_image
from utils import get_status_text


def next_btn_cb(
    label: tk.Label, status: tk.Label, next_cb, image_manager: ImageManager
):
    image = next_cb()
    change_image(label, str(image.path))
    status.config(text=get_status_text(image_manager))
    image_manager.save()


def prev_btn_cb(
    label: tk.Label, status: tk.Label, prev_cb, image_manager: ImageManager
):
    image = prev_cb()
    change_image(label, str(image.path))
    status.config(text=get_status_text(image_manager))
    image_manager.save()


def mark_btn_cb(status: tk.Label, mark_cb, image_manager: ImageManager):
    mark_cb()
    status.config(text=get_status_text(image_manager))
    image_manager.save()


def delete_and_close(image_manager: ImageManager):
    image_manager.delete_on_close()
    image_manager.save()
    sys.exit(0)
