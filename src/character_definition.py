from dataclasses import dataclass, field

@dataclass
class CharacterDefinitionEntry:
    db: str
    value: str

@dataclass
class CharacterDefinition:
    entries: list[CharacterDefinitionEntry] = field(default_factory=list)
