from algorithm.categories import NRUClass, NRUCategory
from constants import MEMORY_PHYSICAL_PAGES_COUNT
from memory.pages import PhysicalPage
from memory.stats import Statistics

PHYSICAL_MEMORY: list[PhysicalPage] = [
    PhysicalPage() for _ in range(MEMORY_PHYSICAL_PAGES_COUNT)
]
FREE_PHYSICAL_MEMORY: list[int] = list(range(len(PHYSICAL_MEMORY)))
BUSY_PHYSICAL_MEMORY: list[int] = []

GLOBAL_STATS: Statistics = Statistics()

NRU_CLASSES_STORAGE: dict[NRUClass, list[int]] = {
    NRUCategory.ZERO: [],
    NRUCategory.FIRST: [],
    NRUCategory.SECOND: [],
    NRUCategory.THIRD: [],
}
