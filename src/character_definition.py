from dataclasses import dataclass, field


@dataclass
class CharacterDefinitionTrait:
    """
    An entry from a trait database.

    Attributes
    ---
    source_db
        Database this entry takes its source from.
    trait_name
        Trait name.
    """
    source_db: str
    "Database this entry takes its source from."
    trait_name: str
    "Trait name."


@dataclass
class CharacterDefinition:
    """
    A whole character definition.
    
    Attributes
    ---
    traits
        List of traits of this character.
    """
    traits: list[CharacterDefinitionTrait] = field(default_factory=list)
