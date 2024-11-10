from dataclasses import dataclass, field
from enum import StrEnum


class DatabaseEntryType(StrEnum):
    BASED = "based"
    EITHER = "either"
    ONEOF = "oneof"
    PERCENT = "percent"
    STACK = "stack"


@dataclass
class CharacterDatabase:
    data: dict = field(default_factory=dict)