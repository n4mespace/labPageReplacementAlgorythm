from dataclasses import dataclass
from enum import Enum


@dataclass
class NRUClass:
    """
    Single NRU class representation.
    """

    R: bool
    M: bool


class NRUCategory(Enum):
    """
    NRU algorithm page classes.
    """

    ZERO: NRUClass = NRUClass(R=False, M=False)
    FIRST: NRUClass = NRUClass(R=False, M=True)
    SECOND: NRUClass = NRUClass(R=True, M=False)
    THIRD: NRUClass = NRUClass(R=True, M=True)
