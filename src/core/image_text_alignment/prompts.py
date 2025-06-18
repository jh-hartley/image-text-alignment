from pathlib import Path

from src.common.exceptions import MalformedPrompt
from src.common.file_readers.txt import read_prompt_from_txt

PROMPT_FILE = Path(__file__).parent / "prompts" / "product_image_system.txt"

try:
    PRODUCT_IMAGE_SYSTEM_PROMPT = read_prompt_from_txt(PROMPT_FILE)
except Exception as e:
    raise MalformedPrompt(
        f"Failed to load product image system prompt: {e}"
    ) from e
