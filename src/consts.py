from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"


WINDOW_HEIGHT = 960
WINDOW_WIDTH = int(WINDOW_HEIGHT * 1.77777778)
IMAGE_CONTAINER_HEIGHT = 800
IMAGE_CONTAINER_WIDTH = int(IMAGE_CONTAINER_HEIGHT * 1.77777778)
SAVE_FILE = DATA_DIR / "save_data.json"

VALID_IMAGE_EXTS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
]
