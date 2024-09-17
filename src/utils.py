from pathlib import Path

from browsed_image import ImageManager
from consts import VALID_IMAGE_EXTS


def get_scaled_size(
    image_width: int, image_height: int, available_width: int, available_height: int
) -> tuple[int, int]:
    aspect_ratio = image_width / image_height
    if available_width / aspect_ratio <= available_height:
        return available_width, int(available_width / aspect_ratio)
    else:
        return int(available_height * aspect_ratio), available_height


def get_images(image_folder: Path) -> list[Path]:
    return [img for img in image_folder.iterdir() if img.suffix in VALID_IMAGE_EXTS]


def get_status_text(image_manager: ImageManager):
    text = f"{image_manager.index+1}/{len(image_manager.browsed_images)}"
    if image_manager.current_image().marked_for_deletion:
        text += "  ❌"
    else:
        text += "  ⬜"
    return text


def delete_on_close(image_manager: ImageManager):
    images_to_delete = [
        img for img in image_manager.browsed_images if img.marked_for_deletion
    ]
    reduce_idx_by = len(images_to_delete)
    for img in images_to_delete:
        img.delete()
    image_manager.index = image_manager.index - reduce_idx_by
