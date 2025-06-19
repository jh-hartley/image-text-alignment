from pathlib import Path

from src.common.exceptions import MalformedPrompt
from src.common.file_readers.txt import read_prompt_from_txt

CLASSIFIER_PROMPT_PATH = Path(__file__).parent / "classifier_prompt.txt"
REFEREE_PROMPT_PATH = Path(__file__).parent / "referee_prompt.txt"

try:
    CLASSIFIER_PROMPT = read_prompt_from_txt(CLASSIFIER_PROMPT_PATH)
    REFEREE_PROMPT = read_prompt_from_txt(REFEREE_PROMPT_PATH)
except Exception as e:
    raise MalformedPrompt(
        f"Failed to load product image system prompt: {e}"
    ) from e
