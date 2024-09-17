import sys
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageTk

from browsed_image import ImageManager
from consts import (
    IMAGE_CONTAINER_HEIGHT,
    IMAGE_CONTAINER_WIDTH,
    SAVE_FILE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from tkinter_btn_callbacks import (
    delete_and_close,
    mark_btn_cb,
    next_btn_cb,
    prev_btn_cb,
)
from tkinter_funcs import add_button, init_root
from utils import get_images, get_scaled_size, get_status_text


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_folder_path>")
        sys.exit(1)
    image_dir = Path(sys.argv[1])
    assert image_dir.is_dir()

    #############
    # Load images
    #############
    image_manager = ImageManager(save_file=SAVE_FILE, image_dir=image_dir)
    image_manager.load_from_paths(get_images(image_dir))
    if len(image_manager.browsed_images) < 1:
        print("No images found in the folder")
        sys.exit(1)
    image_manager.load()

    root = init_root(WINDOW_WIDTH, WINDOW_HEIGHT)

    ########
    # Status
    ########
    status = tk.Label(
        root,
        text=get_status_text(image_manager),
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white",
    )
    status.pack(pady=10)

    #########
    # Buttons
    #########
    button_group = tk.Frame(root, bg="black", bd=2)
    button_group.pack(padx=10, pady=10)
    button_text_and_callbacks = [
        (
            "Previous",
            lambda: prev_btn_cb(
                label, status, image_manager.previous_image, image_manager
            ),
        ),
        (
            "Next",
            lambda: next_btn_cb(label, status, image_manager.next_image, image_manager),
        ),
        (
            "Mark",
            lambda: mark_btn_cb(
                status, image_manager.current_image().toggle_mark, image_manager
            ),
        ),
        ("Delete Marked and Close", lambda: delete_and_close(image_manager)),
    ]
    for i, text_and_callback in enumerate(button_text_and_callbacks):
        add_button(button_group, text_and_callback[0], i, text_and_callback[1])

    ###############
    # Initial Image
    ###############
    pilimg = Image.open(image_manager.current_path_as_str())
    if pilimg.mode != "RGB":
        pilimg = pilimg.convert("RGB")
    old_width, old_height = pilimg.width, pilimg.height
    new_width, new_height = get_scaled_size(
        old_width, old_height, IMAGE_CONTAINER_WIDTH, IMAGE_CONTAINER_HEIGHT
    )
    pilimg = pilimg.resize((new_width, new_height))
    img = ImageTk.PhotoImage(pilimg)
    label = tk.Label(root, image=img)  # type: ignore
    label.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
