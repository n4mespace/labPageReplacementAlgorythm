from dataclasses import dataclass


@dataclass
class Statistics:
    reads: int = 0
    modifications: int = 0
    page_faults: int = 0
    wrote_dirty_pages_to_disk: int = 0
    working_set_page_access: int = 0
    non_working_set_page_access: int = 0
