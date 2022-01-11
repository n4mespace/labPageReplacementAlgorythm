import logging

from constants import PAGE_DAEMON_PAGES_TO_CHECK
from memory.manager import MemoryManagementUnit
from memory.systemwide import BUSY_PHYSICAL_MEMORY, PHYSICAL_MEMORY
from process.daemon.base import BaseDaemon
from random import sample


class PageDaemon(BaseDaemon):
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self.mmu = MemoryManagementUnit(self.pid)

    def run(self) -> None:
        self._logger.info("Page Daemon memory check initiated...\n")
        self._logger.info("▼" * 40)
        self._logger.info("Page Daemon memory check stats:")

        dirty_pages = 0
        referenced_pages = 0

        pages_to_check = sample(
            BUSY_PHYSICAL_MEMORY,
            min(PAGE_DAEMON_PAGES_TO_CHECK, len(BUSY_PHYSICAL_MEMORY)),
        )

        for page_index in pages_to_check:
            self.mmu.algorithm.remove_page_from_classes_storage(page_index)

            page = PHYSICAL_MEMORY[page_index]
            page.VIRTUAL_PAGE.R = False

            referenced_pages += 1

            if page.VIRTUAL_PAGE.M:
                dirty_pages += 1
                self.mmu.algorithm.add_to_first_class(page_index)

            else:
                self.mmu.algorithm.add_to_zero_class(page_index)

        self._logger.info(f"Referenced pages: {referenced_pages}")
        self._logger.info(f"Dirty pages: {dirty_pages}")
        self._logger.info("▲" * 40 + "\n")
