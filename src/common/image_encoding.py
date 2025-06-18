from pathlib import Path
from typing import Union


def image_file_to_bytes(file_path: Union[str, Path]) -> bytes:
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"Image file not found: {file_path}")
    return path.read_bytes()
