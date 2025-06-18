import re
from pathlib import Path

from src.core.image_encoding.dtos import ImageLoadResult


def load_image_bytes_from_url(image_url: str) -> ImageLoadResult:
    match = re.search(r"\.(jpg|jpeg|png|webp|gif)", image_url, re.IGNORECASE)
    trimmed_url = image_url[: match.end()] if match else image_url
    path_obj = Path(trimmed_url)
    if not path_obj.is_file():
        return ImageLoadResult(image_bytes=None, filename=trimmed_url)
    return ImageLoadResult(
        image_bytes=path_obj.read_bytes(), filename=trimmed_url
    )
