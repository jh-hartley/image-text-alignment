import re


def map_image_url_to_local_path(image_url: str) -> str:
    """Map an image URL to a local file path using the mapping table."""
    match = re.search(r"\.(jpg|jpeg|png|webp|gif)", image_url, re.IGNORECASE)
    trimmed_url = image_url[: match.end()] if match else image_url
    return trimmed_url
