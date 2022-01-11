from abc import ABC

from process.abstract import AbstractProcess


class BaseProcess(AbstractProcess, ABC):
    pid: int
