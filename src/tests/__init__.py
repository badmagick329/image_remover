import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))
