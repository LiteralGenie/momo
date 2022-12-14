from pathlib import Path

PROJ_DIR = Path(__file__).parent.parent.parent
SRC_DIR = PROJ_DIR / "src"

CACHE_DIR = SRC_DIR / "cache"
CONFIG_DIR = SRC_DIR / "config"
DATA_DIR = SRC_DIR / "data"
LOG_DIR = SRC_DIR / "logs"

for name, path in list(locals().items()):
    if name.endswith("_DIR"):
        path.mkdir(exist_ok=True)
