from enum import Enum

# enum
class IsDone(str, Enum):
    def __str__(self):
        return str(self.value)
    INPROGRESS = "IN PROGRESS"
    DONE = "DONE"