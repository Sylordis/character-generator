import logging
from pathlib import Path
import random
from typing import Any

from .character_definition import CharacterDefinition, CharacterDefinitionTrait
from .character_database import TraitDatabase, DatabaseTraitType, MainDatabase
from .parsers.db_parser import DatabaseParser
from .parsers.definition_parser import DefinitionParser
from .parsers.yaml_tags import YAMLtags


class CharacterGenerator:
    """
    Main class for the character generation.

    Attributes
    ---
    dbs
        All database files needed.
    definition
        Definition file for the generation.
    """

    def __init__(self, dbs: list[Path], definition_file: Path):
        """
        Creates a new character generator.

        :param dbs: list of paths that form the database
        :param definition: path to definition file
        """
        db_parser: DatabaseParser = DatabaseParser()
        self.dbs: dict[str, MainDatabase] = {file.name: db_parser.parse(file) for file in dbs}
        self.definition: CharacterDefinition = DefinitionParser().parse(definition_file)
        self.log = logging.getLogger(self.__class__.__name__)

    def generate(self, n: int = 1):
        """
        Generates a character from the definition.

        :param n: number of characters to generate (default 1).
        """
        for i in range(1, n + 1):
            if n > 1:
                print(f"Character {i}:")
            for entry in self.definition.traits:
                self.generate_trait(entry)
            if n > 1 and i != n:
                print("")

    def generate_trait(self, char_trait: CharacterDefinitionTrait):
        """
        Generate one entry of a character definition.

        :param entry: the entry to generate.
        """
        self.log.debug(f"Generating entry '{char_trait.trait_name}' from '{char_trait.source_db}'")
        source_db: MainDatabase = self.dbs.get(char_trait.source_db)
        if char_trait.source_db in self.dbs and char_trait.trait_name in source_db.data:
            trait_db: TraitDatabase = source_db.data.get(char_trait.trait_name)
            trait_name = trait_db.name
            self.log.debug(f"name={trait_name}, types={trait_db.types}")
            value = self.generate_trait_value(trait_db)
            if trait_name is not None:
                print(f"{trait_name}: {value}")
            else:
                print(f"{value}")
        else:
            if char_trait.source_db not in self.dbs:
                self.log.error(f"Couldn't find database '{char_trait.source_db}'.")
            elif char_trait.trait_name not in self.dbs.get(char_trait.source_db).data:
                self.log.error(f"Couldn't find definition of trait '{char_trait.trait_name}'.")

    def generate_trait_value(self, trait_db: TraitDatabase) -> Any:
        """
        Generates the value for a given trait according to its definition.

        :param trait_db: the trait database to calculate the value of.
        """
        value = None
        curr_value = None
        base_value = None
        if DatabaseTraitType.EITHER in trait_db.types:
            value = self.value_for_either(trait_db.data)
        if DatabaseTraitType.PERCENT in trait_db.types:
            curr_value = random.random()
            self.log.debug(f"percent {curr_value}")
        if DatabaseTraitType.STACK in trait_db.types:
            # Take current value and compare to stacks
            value = self.value_for_stacks(curr_value, trait_db.data.get(YAMLtags.DB_VALUES))
        if DatabaseTraitType.ONEOF in trait_db.types:
            value = self.value_for_oneof(trait_db.data.get(YAMLtags.DB_VALUES))
        if value is None:
            # TODO check for base
            value = curr_value
            if DatabaseTraitType.PERCENT in trait_db.types:
                value = "{:.0%}".format(value)
        return value

    def value_for_stacks(self, ref_value: float, stacks: list) -> Any:
        self.log.debug(f"stacks curr_value={ref_value}, stacks={stacks}")
        it = iter(stacks)
        stack: dict = None
        stacked_value: float = -1.0  # in case ref_value = 0
        while ref_value > stacked_value:
            stack = next(it)
            if stacked_value == -1:
                stacked_value = 0
            stacked_value += self.interpret_number(stack.get(YAMLtags.DB_CHANCES))
            self.log.debug(f"{ref_value} <?= {stacked_value}, {stack}")
        self.log.debug(f"end {ref_value} <= {stacked_value}, {stack}")
        actual_value = (
            stack.get(YAMLtags.DB_TEXT) if YAMLtags.DB_TEXT in stack else stack.get(YAMLtags.DB_KEY)
        )
        return actual_value

    def value_for_either(self, data: dict) -> Any:
        all_keys: list = data.get(YAMLtags.DB_KEYS)
        default_key = data.get(YAMLtags.DB_DEFAULT_KEY)
        curr_key = default_key
        self.log.debug(f"either => {curr_key}")
        return self.generate_trait_value(DatabaseParser().create_trait_db(data.get(curr_key)))

    def value_for_oneof(self, values: list) -> Any:
        return random.choice(values)

    def interpret_number(self, value) -> float:
        interpreted = value
        if type(value) is str and "%" in value:
            interpreted = float(value.strip("%")) / 100
        return interpreted
