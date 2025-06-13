from typing import Callable

LLM_PROVIDERS: dict[str, type] = {}
EMBEDDING_PROVIDERS: dict[str, type] = {}


def register_llm_provider(name: str) -> Callable[[type], type]:
    def decorator(cls: type) -> type:
        LLM_PROVIDERS[name] = cls
        return cls

    return decorator


def register_embedding_provider(name: str) -> Callable[[type], type]:
    def decorator(cls: type) -> type:
        EMBEDDING_PROVIDERS[name] = cls
        return cls

    return decorator
