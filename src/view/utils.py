import os
from pathlib import Path


def gui_root() -> Path:
    """Returns gui root folder."""
    return Path(__file__).parent.parent.parent
