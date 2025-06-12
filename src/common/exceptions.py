class MalformedPrompt(Exception):
    """Raised when a prompt file is malformed or cannot be read."""

    pass


class ImageProcessingError(Exception):
    """Base exception for image processing errors."""

    pass


class PredictionError(ImageProcessingError):
    """Raised when prediction fails."""

    pass
