import os.path
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

ROOT_PATH = Path(ROOT_DIR).absolute()
DATA_PATH = ROOT_PATH / "data"
WEB_PATH = ROOT_PATH / "web"