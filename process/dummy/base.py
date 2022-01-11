from abc import ABC
from random import randrange

from constants import PROCESS_AVG_WORKING_TIME, PROCESS_WORKING_TIME_DEVIATION
from process.base import BaseProcess


class BaseDummyProcess(BaseProcess, ABC):
    working_time: int = 0
    finished: bool = False
    blocked: bool = False

    @staticmethod
    def generate_working_time() -> int:
        return randrange(
            PROCESS_AVG_WORKING_TIME - PROCESS_WORKING_TIME_DEVIATION,
            PROCESS_AVG_WORKING_TIME + PROCESS_WORKING_TIME_DEVIATION,
        )
