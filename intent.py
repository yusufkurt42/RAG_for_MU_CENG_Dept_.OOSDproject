from enum import Enum, auto

class Intent(Enum):
    REGISTRATION = auto()
    STAFF_LOOKUP = auto()
    POLICY_FAQ = auto()
    COURSE = auto()
    UNKNOWN = auto()
