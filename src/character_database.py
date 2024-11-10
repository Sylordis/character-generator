from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path


class DatabaseTraitDisplayType(StrEnum):
    DEFAULT = "default"
    CASCADE_ONLY = "cascade_only"


class DatabaseTraitType(StrEnum):
    BASED = "based"
    EITHER = "either"
    ONEOF = "oneof"
    PERCENT = "percent"
    STACK = "stack"


@dataclass
class TraitDatabase:
    name: str
    display: DatabaseTraitDisplayType = DatabaseTraitDisplayType.DEFAULT
    types: list[DatabaseTraitType] = field(default_factory=list)
    data: dict = field(default_factory=dict)

@dataclass
class MainDatabase:
    name: str
    file: Path
    data: dict[str,TraitDatabase] = field(default_factory=dict)