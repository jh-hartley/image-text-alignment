import logging
from typing import Callable, Type

from src.common.logging import setup_logging

logger = logging.getLogger(__name__)
setup_logging()

# Registry for providers
PROVIDERS: dict[str, dict[str, Type]] = {
    "llm": {},
    "embedding": {},
    "image_processor": {},
}


def register_provider(provider_type: str, name: str) -> Callable[[Type], Type]:
    """Register a provider class with the given name."""

    def decorator(cls: Type) -> Type:
        if provider_type not in PROVIDERS:
            raise ValueError(f"Unknown provider type: {provider_type}")
        PROVIDERS[provider_type][name] = cls
        logger.debug(f"Registered {provider_type} provider: {name}")
        logger.debug(
            f"Current {provider_type} providers: "
            f"{list(PROVIDERS[provider_type].keys())}"
        )
        return cls

    return decorator


def get_provider(provider_type: str, name: str) -> Type:
    """Get a provider class by name."""
    if provider_type not in PROVIDERS:
        raise ValueError(f"Unknown provider type: {provider_type}")
    if name not in PROVIDERS[provider_type]:
        raise ValueError(f"Unknown {provider_type} provider: {name}")
    return PROVIDERS[provider_type][name]
