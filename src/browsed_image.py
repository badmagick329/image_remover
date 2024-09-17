import json
from pathlib import Path

from pydantic import BaseModel, field_serializer


class BrowsedImage(BaseModel):
    path: Path
    marked_for_deletion: bool = False
    _deleted: bool | None = None

    @field_serializer("path")
    def serialize_path(self, path: Path) -> str:
        return str(path)

    @property
    def deleted(self) -> bool:
        if self._deleted is None:
            self._deleted = self.path.is_file()
        return self._deleted

    def delete(self) -> bool:
        try:
            self.path.unlink()
            self._deleted = True
            return True
        except (FileNotFoundError, PermissionError):
            return False

    def toggle_mark(self):
        self.marked_for_deletion = not self.marked_for_deletion
        return self


class ImageManager:
    browsed_images: list[BrowsedImage]
    _loaded_data: dict
    _image_dir: Path
    _save_file: Path
    _index: int

    def __init__(
        self,
        save_file: Path,
        image_dir: Path,
        browsed_images: list[BrowsedImage] | None = None,
    ) -> None:
        self._save_file = save_file
        self._image_dir = image_dir
        self.browsed_images = browsed_images or list()
        self._index = 0
        self._loaded_data = dict()

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        if value < 0:
            self._index = 0
        elif value >= len(self.browsed_images):
            self._index = len(self.browsed_images) - 1
        else:
            self._index = value

    def save(self):
        data_dump = ([bi.model_dump() for bi in self.browsed_images],)
        with open(self._save_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    **self._loaded_data,
                    str(self._image_dir): {"index": self._index, "data": data_dump},
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    def load_from_paths(self, paths: list[Path]):
        self.browsed_images = [BrowsedImage(path=path) for path in paths]

    def load(self):
        with open(self._save_file, "r", encoding="utf-8") as f:
            self._loaded_data = json.load(f)
        found_data = self._loaded_data.get(str(self._image_dir))
        if found_data:
            self.index = found_data["index"]
            self.browsed_images = [
                BrowsedImage(**bi)
                for bi in found_data["data"][0]
                if Path(bi["path"]).is_file()
            ]
        else:
            self.browsed_images = list()

    def current_path(self) -> Path:
        if not self.browsed_images:
            raise ValueError("No images loaded")
        return self.browsed_images[self._index].path

    def current_path_as_str(self) -> str:
        return str(self.current_path())

    def current_image(self) -> BrowsedImage:
        if not self.browsed_images:
            raise ValueError("No images loaded")
        return self.browsed_images[self._index]

    def next_image(self) -> BrowsedImage:
        if not self.browsed_images:
            raise ValueError("No images loaded")
        self._index += 1
        if self._index >= len(self.browsed_images):
            self._index = 0
        return self.current_image()

    def previous_image(self) -> BrowsedImage:
        if not self.browsed_images:
            raise ValueError("No images loaded")
        self._index -= 1
        if self._index < 0:
            self._index = len(self.browsed_images) - 1

        return self.current_image()

    def delete_on_close(self):
        images_to_delete = [
            img for img in self.browsed_images if img.marked_for_deletion
        ]
        reduce_idx_by = len(images_to_delete)
        for img in images_to_delete:
            img.delete()
        self.index = self.index - reduce_idx_by
