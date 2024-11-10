import logging
from pathlib import Path
import random
from typing import Any

from .character_definition import CharacterDefinition, CharacterDefinitionEntry
from .character_database import CharacterDatabase, DatabaseEntryType
from .parsers.db_parser import DataBaseParser
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
        db_parser: DataBaseParser = DataBaseParser()
        self.dbs: dict[str,CharacterDatabase] = {file.name: db_parser.parse(file) for file in dbs}
        self.definition: CharacterDefinition = DefinitionParser().parse(definition_file)
        self.log = logging.getLogger(self.__class__.__name__)

    def generate(self, n: int = 1):
        """
        Generates a character from the definition.

        :param n: number of characters to generate (default 1).
        """
        for i in range(n):
            for entry in self.definition.entries:
                self.generate_entry(entry)

    def generate_entry(self, char_entry: CharacterDefinitionEntry):
        """
        Generate one entry of a character definition.

        :param entry: the entry to generate.
        """
        self.log.debug(f"Generating entry '{char_entry.value}' from '{char_entry.db}'")
        corresponding_db: dict = self.dbs.get(char_entry.db).data.get(char_entry.value)
        db_name = corresponding_db.get(YAMLtags.DB_NAME)
        self.log.debug(f"name={db_name}, types={corresponding_db.get(YAMLtags.DB_TYPE)}")
        value = self.calculate_entry_value(corresponding_db)
        if db_name is not None:
            print(f"{db_name}: {value}")
        else:
            print(f"{value}")

    def calculate_entry_value(self, db: dict) -> Any:
        value = None
        curr_value = None
        db_types: list = db.get(YAMLtags.DB_TYPE)
        if DatabaseEntryType.EITHER in db_types:
            value = self.value_for_either(db)
        if DatabaseEntryType.PERCENT in db_types:
            curr_value = random.random()
            self.log.debug(f"percent {curr_value}")
        if DatabaseEntryType.STACK in db_types:
            # Take current value and compare to stacks
            value = self.value_for_stacks(curr_value, db.get(YAMLtags.DB_VALUES))
        if DatabaseEntryType.ONEOF in db_types:
            value = self.value_for_oneof(db)
        if value is None:
            # TODO check for base
            value = curr_value
            if DatabaseEntryType.PERCENT in db_types:
                value = "{:.0%}".format(value)
        return value

    def value_for_stacks(self, ref_value: float, stacks: list) -> Any:
        self.log.debug(f"stacks curr_value={ref_value}, stacks={stacks}")
        it = iter(stacks)
        stack: dict = None
        stacked_value: float = -1.0 # in case ref_value = 0
        while ref_value > stacked_value:
            stack = next(it)
            if stacked_value == -1:
                stacked_value = 0
            stacked_value += self.interpret_number(stack.get(YAMLtags.DB_CHANCES))
            self.log.debug(f"{ref_value} <?= {stacked_value}, {stack}")
        self.log.debug(f"end {ref_value} <= {stacked_value}, {stack}")
        actual_value = stack.get(YAMLtags.DB_TEXT) if YAMLtags.DB_TEXT in stack else stack.get(YAMLtags.DB_KEY)
        return actual_value

    def value_for_either(self, data: dict) -> Any:
        all_keys: list = data.get(YAMLtags.DB_KEYS)
        default_key = data.get(YAMLtags.DB_DEFAULT_KEY)
        curr_key = default_key
        self.log.debug(f"either => {curr_key}")
        return self.calculate_entry_value(data.get(curr_key))

    def value_for_oneof(self, data: dict) -> Any:
        possible_values = data.get(YAMLtags.DB_VALUES)
        return random.choice(possible_values)
    
    def interpret_number(self, value) -> float:
        interpreted = value
        if type(value) is str and "%" in value:
            interpreted = float(value.strip("%"))/100
        return interpreted
            
