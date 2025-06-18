import random


def get_rng(seed: int | None = None) -> random.Random:
    if seed is not None:
        return random.Random(seed)
    return random.Random()
