from algorithm.categories import NRUCategory, NRUClass
from memory.systemwide import (
    NRU_CLASSES_STORAGE,
    FREE_PHYSICAL_MEMORY,
    BUSY_PHYSICAL_MEMORY,
    PHYSICAL_MEMORY,
)


class NRUCategoriesAlgorithm:
    @staticmethod
    def _remove_from_class(nru_class: NRUClass, page_index: int):
        NRU_CLASSES_STORAGE[nru_class].remove(page_index)

    def remove_from_zero_class(self, page_index: int) -> None:
        self._remove_from_class(NRUCategory.ZERO, page_index)

    def remove_from_first_class(self, page_index: int) -> None:
        self._remove_from_class(NRUCategory.FIRST, page_index)

    def remove_from_second_class(self, page_index: int) -> None:
        self._remove_from_class(NRUCategory.SECOND, page_index)

    @staticmethod
    def remove_page_from_classes_storage(page_index: int) -> None:
        for pages in NRU_CLASSES_STORAGE.values():
            if page_index in pages:
                pages.remove(page_index)

    @staticmethod
    def _add_to_class(nru_class: NRUClass, page_index: int):
        NRU_CLASSES_STORAGE[nru_class].append(page_index)

    def add_to_zero_class(self, page_index: int) -> None:
        self._add_to_class(NRUCategory.ZERO, page_index)

    def add_to_first_class(self, page_index: int) -> None:
        self._add_to_class(NRUCategory.FIRST, page_index)

    def add_to_second_class(self, page_index: int) -> None:
        self._add_to_class(NRUCategory.SECOND, page_index)

    def add_to_third_class(self, page_index: int) -> None:
        self._add_to_class(NRUCategory.THIRD, page_index)

    def handle_zero_class(self, page_index: int) -> bool:
        physical_page = PHYSICAL_MEMORY[page_index]
        self.remove_from_zero_class(page_index)

        if not physical_page.VIRTUAL_PAGE.M and not physical_page.VIRTUAL_PAGE.R:
            return True

        if physical_page.VIRTUAL_PAGE.M and physical_page.VIRTUAL_PAGE.R:
            self.add_to_third_class(page_index)
        elif physical_page.VIRTUAL_PAGE.R:
            self.add_to_second_class(page_index)
        else:
            self.add_to_first_class(page_index)

        return False

    def handle_first_class(self, page_index: int) -> bool:
        physical_page = PHYSICAL_MEMORY[page_index]
        self.remove_from_first_class(page_index)

        if not physical_page.VIRTUAL_PAGE.R:
            return True

        if physical_page.VIRTUAL_PAGE.M:
            self.add_to_third_class(page_index)
        else:
            self.add_to_second_class(page_index)

        return False

    def handle_second_class(self, page_index: int) -> bool:
        physical_page = PHYSICAL_MEMORY[page_index]
        self.remove_from_second_class(page_index)

        if not physical_page.VIRTUAL_PAGE.M:
            return True

        if physical_page.VIRTUAL_PAGE.R:
            self.add_to_third_class(page_index)

        return False

    @staticmethod
    def pop_from_third_class() -> int:
        return NRU_CLASSES_STORAGE[NRUCategory.THIRD].pop(0)

    def find_free_page(self) -> int:
        if FREE_PHYSICAL_MEMORY:
            page_index = FREE_PHYSICAL_MEMORY[0]

            FREE_PHYSICAL_MEMORY.remove(page_index)
            BUSY_PHYSICAL_MEMORY.append(page_index)

            return page_index

        for category, page_indexes in NRU_CLASSES_STORAGE.items():
            for page_index in page_indexes:
                if (
                    (
                        category == NRUCategory.ZERO
                        and self.handle_zero_class(page_index)
                    )
                    or (
                        category == NRUCategory.FIRST
                        and self.handle_first_class(page_index)
                    )
                    or (
                        category == NRUCategory.SECOND
                        and self.handle_second_class(page_index)
                    )
                ):
                    return page_index

        return self.pop_from_third_class()
