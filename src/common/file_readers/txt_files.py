from pathlib import Path

from src.common.exceptions import MalformedPrompt


def read_prompt_from_txt(
    file_path: str | Path, encoding: str = "utf-8"
) -> str:
    try:
        with open(file_path, "r", encoding=encoding) as f:
            content = f.read().strip()

        if not content:
            raise MalformedPrompt(f"File is empty: {file_path}")

        return content

    except FileNotFoundError as err:
        raise MalformedPrompt(f"File not found: {file_path}") from err
    except UnicodeDecodeError as err:
        raise MalformedPrompt(
            f"File encoding error in {file_path}. Expected {encoding}"
        ) from err
    except Exception as err:
        raise MalformedPrompt(
            f"Error reading file {file_path}: {str(err)}"
        ) from err
