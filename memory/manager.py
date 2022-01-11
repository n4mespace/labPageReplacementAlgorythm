import logging
from random import randint, random, sample, choice

from algorithm.nru import NRUCategoriesAlgorithm
from constants import (
    WORKING_SET_PAGES_INITIAL_COUNT,
    PROCESS_WORKING_SET_PAGE_ACCESS_PROB,
    MAX_VIRTUAL_PAGES,
    MIN_VIRTUAL_PAGES,
)
from memory.pages import VirtualPage
from memory.systemwide import (
    GLOBAL_STATS,
    PHYSICAL_MEMORY,
    FREE_PHYSICAL_MEMORY,
    BUSY_PHYSICAL_MEMORY,
)


class MemoryManagementUnit:
    def __init__(self, pid: int) -> None:
        self._pid = pid
        self._logger = logging.getLogger(__name__)

        self.algorithm: NRUCategoriesAlgorithm = NRUCategoriesAlgorithm()

        self._virtual_memory = [
            VirtualPage(P=False, R=False, M=False, PPN=None)
            for _ in range(randint(MIN_VIRTUAL_PAGES, MAX_VIRTUAL_PAGES))
        ]
        self._working_set_page_indexes = sample(
            list(range(len(self._virtual_memory))),
            WORKING_SET_PAGES_INITIAL_COUNT,
        )
        self._non_working_set_page_indexes = list(
            set(range(len(self._virtual_memory))) - set(self._working_set_page_indexes)
        )

    def _load_page_to_memory(self, page: VirtualPage) -> None:
        ppn = self.algorithm.find_free_page()

        self._free_old_virtual_page(PHYSICAL_MEMORY[ppn].VIRTUAL_PAGE)
        self._update_new_page(page, ppn)

    def _free_old_virtual_page(self, old_page: VirtualPage) -> None:
        if old_page:
            if old_page.M:
                GLOBAL_STATS.wrote_dirty_pages_to_disk += 1
                self._logger.info(
                    f"Writing dirty page to disc: Process id: [{self._pid}]"
                )

            old_page.P = False
            old_page.R = False
            old_page.M = False
            old_page.PPN = None

    def _update_new_page(self, page: VirtualPage, ppn: int) -> None:
        page.P = True
        page.M = False
        page.R = False
        page.PPN = ppn

        PHYSICAL_MEMORY[ppn].VIRTUAL_PAGE = page

    def _get_access_page_num(self):
        if random() < PROCESS_WORKING_SET_PAGE_ACCESS_PROB:
            GLOBAL_STATS.working_set_page_access += 1
            self._logger.info(f"Working set page access: Process id: [{self._pid}]")

            return choice(self._working_set_page_indexes)

        else:
            GLOBAL_STATS.non_working_set_page_access += 1
            self._logger.info(f"Not working set page access: Process id: [{self._pid}]")

            return choice(self._non_working_set_page_indexes)

    def _check_page_operation(self) -> int:
        vpn = self._get_access_page_num()
        page = self._virtual_memory[vpn]

        if not page.P:
            GLOBAL_STATS.page_faults += 1

            self._logger.info(f"Page fault: Process id: [{self._pid}]")
            self._load_page_to_memory(page)

        return vpn

    def read_page(self) -> None:
        vpn = self._check_page_operation()

        self._virtual_memory[vpn].R = True

        GLOBAL_STATS.reads += 1
        self._logger.info(f"Page read: Process id: [{self._pid}]")

    def modify_page(self) -> None:
        vpn = self._check_page_operation()

        self._virtual_memory[vpn].M = True
        self._virtual_memory[vpn].R = True

        GLOBAL_STATS.modifications += 1
        self._logger.info(f"Page modification: Process id: [{self._pid}]")

    def free_memory(self) -> None:
        for virtual_page in self._virtual_memory:
            if virtual_page.P:
                BUSY_PHYSICAL_MEMORY.remove(virtual_page.PPN)
                FREE_PHYSICAL_MEMORY.append(virtual_page.PPN)
                self.algorithm.remove_page_from_classes_storage(virtual_page.PPN)

                PHYSICAL_MEMORY[virtual_page.PPN].VIRTUAL_PAGE = None
