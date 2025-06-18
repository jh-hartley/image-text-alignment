from pathlib import Path

from sqlalchemy.orm import Session

from src.core.image_text_alignment.dtos import ImageLoadResult

from .filepath_mapping import map_image_url_to_filename


def load_image_bytes_from_url(
    session: Session, image_url: str
) -> ImageLoadResult:
    """
    Return an ImageLoadResult for a given image_url.
    """
    filename = map_image_url_to_filename(session, image_url)
    if not filename:
        return ImageLoadResult(image_bytes=None, filename=None)
    local_path = Path("data/image") / filename
    if not local_path.is_file():
        return ImageLoadResult(image_bytes=None, filename=filename)
    return ImageLoadResult(
        image_bytes=local_path.read_bytes(), filename=filename
    )
