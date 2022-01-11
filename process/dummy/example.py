import logging
from random import random

from constants import (
    PROCESS_ACCESS_MODIFY_PAGE_PROB,
)
from memory.manager import MemoryManagementUnit
from process.dummy.base import BaseDummyProcess


class DummyProcess(BaseDummyProcess):
    def __init__(self, pid: int, process_time: int) -> None:
        self._process_time = process_time
        self._logger = logging.getLogger(__name__)

        self.pid = pid
        self.mmu = MemoryManagementUnit(self.pid)

    def _access_page(self):
        if random() < PROCESS_ACCESS_MODIFY_PAGE_PROB:
            self.mmu.modify_page()
        else:
            self.mmu.read_page()

    def run(self) -> None:
        self._logger.info(f"Process [{self.pid}] running")

        self._access_page()
        self.working_time += 1

        if self._process_time == self.working_time:
            self.mmu.free_memory()
            self.finished = True

            self._logger.info(f"Process [{self.pid}] finished")
