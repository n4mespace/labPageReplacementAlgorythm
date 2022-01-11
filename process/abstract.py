from abc import ABC, abstractmethod


class AbstractProcess(ABC):
    """
    Abstract process class.
    """

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError("Should implement Process `run` method.")
