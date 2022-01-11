import logging
from collections import deque as RR_queue
from random import random
from typing import Optional, Any

from constants import (
    PROCESS_STARTING_PID,
    SIMULATION_TICKS,
    INITIAL_PROCESSES,
    PAGE_DAEMON_CHECKS_PERIOD,
    PROCESS_SPAWN_PROB,
    PROCESS_QUANT,
)
from memory.systemwide import GLOBAL_STATS
from process.daemon.base import BaseDaemon
from process.daemon.page import PageDaemon
from process.dummy.base import BaseDummyProcess
from process.dummy.example import DummyProcess


class OneProcessSystem:
    # System & Process counters.
    current_tick: int = 0
    pid_count: int = PROCESS_STARTING_PID
    current_process: Optional[BaseDummyProcess] = None

    def __init__(self) -> None:
        self._processes: RR_queue[BaseDummyProcess] = RR_queue()
        self._daemons: list[BaseDaemon] = []

        self._logger = logging.getLogger(__name__)

    def __enter__(self) -> "OneProcessSystem":
        """
        System resources initialization.
        """

        self._generate_processes()
        self._generate_daemons()

        self._logger.info("Initialization of system resources is completed.")

        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """
        System resources clean up.
        """

        self._processes.clear()
        self._daemons.clear()

        self._logger.info("Finishing simulation...\n")

        self._logger.info("▼" * 40)
        self._logger.info("Simulation global stats:")
        self._logger.info(f"Processes: {self.pid_count}")
        self._logger.info(
            f"Working set page accesses: [{GLOBAL_STATS.working_set_page_access}]"
        )
        self._logger.info(
            f"Non working set page accesses: [{GLOBAL_STATS.non_working_set_page_access}]"
        )
        self._logger.info(f"Reads: [{GLOBAL_STATS.reads}]")
        self._logger.info(f"Modifications: [{GLOBAL_STATS.modifications}]")
        self._logger.info(f"Page faults: [{GLOBAL_STATS.page_faults}]")
        self._logger.info(
            f"Dirty pages writes to disk: [{GLOBAL_STATS.wrote_dirty_pages_to_disk}]"
        )
        self._logger.info("▲" * 40 + "\n")

        self._logger.info("System resources was cleaned up.")

    def _generate_daemons(self) -> None:
        self._daemons = [PageDaemon()]

    def _generate_processes(self) -> None:
        for _ in range(INITIAL_PROCESSES):
            self._spawn_process()

    def _spawn_process(self) -> None:
        self._processes.append(
            DummyProcess(self.pid_count, BaseDummyProcess.generate_working_time())
        )
        self.pid_count += 1

    def _run_daemons(self) -> None:
        for daemon in self._daemons:
            daemon.run()

    def run_simulation(self) -> None:
        for tick in range(1, SIMULATION_TICKS + 1):
            self._logger.info(f"Tick [{tick}]...")
            self._logger.info(f"Processes count: [{self.pid_count}]")

            self.current_tick = tick

            if not tick % PAGE_DAEMON_CHECKS_PERIOD:
                self._run_daemons()

            self.check_processes()
            self.current_process.run()

            self._logger.info("-" * 40)

    def check_processes(self) -> None:
        if not len(self._processes):
            self._spawn_process()

        if (
            self.current_tick % PROCESS_QUANT == 0
            or self.current_process
            and (self.current_process.finished or self.current_process.blocked)
        ):
            if not self.current_process.finished:
                self._processes.append(self.current_process)

            self.current_process = None

        if not self.current_process:
            self.current_process = self._processes.popleft()

            while self.current_process.blocked:
                self._processes.append(self.current_process)
                self.current_process = self._processes.popleft()

        if random() < PROCESS_SPAWN_PROB:
            self._spawn_process()
