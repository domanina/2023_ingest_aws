from enum import Enum


class ExtendedEnum(Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class Colors(ExtendedEnum):
    BLACK = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[92m"
    YELLOW = "\033[33m"


class TaskStates(ExtendedEnum):
    NEW = "NEW"
    TAKEN = "TAKEN"
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"
    PAUSED = "PAUSED"


TIMEOUT_SEC = 5
RETRY = 100
