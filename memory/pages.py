from dataclasses import dataclass
from typing import Optional


@dataclass
class VirtualPage:
    R: bool = False
    M: bool = False
    P: bool = False
    PPN: Optional[int] = None


@dataclass
class PhysicalPage:
    VIRTUAL_PAGE: Optional[VirtualPage] = None
