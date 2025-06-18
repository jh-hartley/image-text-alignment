import re

from sqlalchemy.orm import Session

from src.core.data_ingestion.repositories import ImageFilePathMappingRepository


def map_image_url_to_filename(session: Session, image_url: str) -> str | None:
    """Map an image URL to a local filename using the mapping table."""
    if not image_url:
        return None
    match = re.search(r"\.(jpg|jpeg|png|webp|gif)", image_url, re.IGNORECASE)
    trimmed_url = image_url[: match.end()] if match else image_url
    repo = ImageFilePathMappingRepository(session)
    mapping = repo.find(image_url=trimmed_url)
    if mapping:
        return mapping[0].to_dto().image_path.replace("\\", "/").split("/")[-1]
    return None
