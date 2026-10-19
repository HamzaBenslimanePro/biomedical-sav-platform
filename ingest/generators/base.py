"""Shared helpers for all generators.

Kept intentionally tiny: this is the *only* place `weighted_choice` lives, so
every generator picks from the same implementation and the same underlying
`random.Random`. Do not re-implement this in individual generator modules.
"""

from __future__ import annotations
import random
from typing import TypeVar

T = TypeVar("T")


def weighted_choice(rng: random.Random, weights: dict[T, int]) -> T:
    """Pick one key from ``weights`` where values are relative weights.

    Example
    -------
    >>> rng = random.Random(42)
    >>> weighted_choice(rng, {"A": 90, "B": 10})  # doctest: +SKIP
    'A'

    Notes
    -----
    * Weights do not need to sum to 100; ``random.choices`` normalizes them.
    * Raises ``ValueError`` on an empty dict — fail loudly, not with ``IndexError``.
    * Uses the caller's ``rng`` so seeded reproducibility holds across tables.
    """
    if not weights:
        raise ValueError("weighted_choice: weights dict is empty")
    keys = list(weights.keys())
    return rng.choices(keys, weights=list(weights.values()), k=1)[0]