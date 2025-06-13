import importlib
import logging
import pkgutil

from src.common.logs import setup_logging

from .embedding import Embedding
from .image_processor import get_processor
from .llm import Llm

logger = logging.getLogger(__name__)
setup_logging()

for _, name, is_pkg in pkgutil.iter_modules(__path__, __name__ + "."):
    if is_pkg and name.endswith(".providers"):
        try:
            importlib.import_module(name)
            logger.debug(f"Imported provider package: {name}")
        except ImportError as e:
            logger.warning(f"Failed to import provider package {name}: {e}")

__all__ = ["Llm", "Embedding", "get_processor"]
