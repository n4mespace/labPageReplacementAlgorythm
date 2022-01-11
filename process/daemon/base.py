from abc import ABC

from constants import PAGE_DAEMON_PID
from process.base import BaseProcess


class BaseDaemon(BaseProcess, ABC):
    pid: int = PAGE_DAEMON_PID
