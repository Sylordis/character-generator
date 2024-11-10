import logging
from pathlib import Path
import random
from typing import Any

from .character_definition import CharacterDefinition, CharacterDefinitionTrait
from .character_database import TraitDatabase, DatabaseTraitType, MainDatabase, DatabaseTraitDisplayType
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
    opts
        Arguments passed from the ArgParser.
    """

    def __init__(self, dbs: list[Path], definition_file: Path, opts = None):
        """
        Creates a new character generator.

        :param dbs: list of paths that form the database
        :param definition: path to definition file
        """
        db_parser: DatabaseParser = DatabaseParser()
        self.dbs: dict[str, MainDatabase] = {file.name: db_parser.parse(file) for file in dbs}
        self.definition: CharacterDefinition = DefinitionParser().parse(definition_file)
        self.opts = opts
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
                triggers: dict = self.generate_trait(entry)
            if n > 1 and i != n:
                print("")

    def generate_trait(self, char_trait: CharacterDefinitionTrait) -> dict:
        """
        Generate one entry of a character definition.

        :param char_trait: the entry to generate.
        :return: the definitions of triggers.
        """
        self.log.debug(f"Generating entry '{char_trait.trait_name}' from '{char_trait.source_db}'")
        source_db: MainDatabase = self.dbs.get(char_trait.source_db)
        cascades = {}
        cascades_result = []
        triggers = {}
        if char_trait.source_db in self.dbs and char_trait.trait_name in source_db.data:
            trait_db: TraitDatabase = source_db.data.get(char_trait.trait_name)
            self.log.debug(f"name={trait_db.name}, types={trait_db.types}")
            value, cascades, triggers = self.generate_trait_value(trait_db)
            self.log.debug(f"value={value}, cascades={cascades}")
            if cascades:
                for trait_name, n in cascades.items():
                    for i in range(n):
                        c_value, _, _ = self.generate_trait_value(source_db.data.get(trait_name))
                        cascades_result.append(c_value)
            self.print_trait_result(trait_db, value, cascades_result)
        else:
            if char_trait.source_db not in self.dbs:
                self.log.error(f"Couldn't find database '{char_trait.source_db}'.")
            elif char_trait.trait_name not in source_db.data and not self.opts.ignore_undefined:
                self.log.error(f"Couldn't find definition of trait '{char_trait.trait_name}'.")
        return triggers

    def print_trait_result(self, trait_db: TraitDatabase, value, cascades: list):
        """
        Manages the printing process of a trait result.

        :param trait_db: the trait to print
        :param value: the value generated for this trait
        :param cascades: all cascades values
        """
        display_value = f"{trait_db.name}:"
        if cascades and trait_db.display == DatabaseTraitDisplayType.CASCADE_ONLY:
            display_value = display_value + f" {', '.join(cascades)}"
        elif cascades:
            display_value = display_value + f" {value} ({', '.join(cascades)})"
        else:
            display_value = display_value + f" {value}"
        print(display_value)

    def generate_trait_value(self, trait_db: TraitDatabase) -> tuple[Any,dict,dict]:
        """
        Generates the value for a given trait according to its definition.

        :param trait_db: the trait database to calculate the value of.
        :return: a triplet [value, cascades definitions, triggers definitions].
        """
        value = None
        curr_value = None
        base_value = None
        cascades = {}
        triggers = {}
        if DatabaseTraitType.EITHER in trait_db.types:
            value, cascades, triggers = self.value_for_either(trait_db.data)
        if DatabaseTraitType.PERCENT in trait_db.types:
            curr_value = random.random()
            self.log.debug(f"percent {curr_value}")
        if DatabaseTraitType.STACK in trait_db.types:
            # Take current value and compare to stacks
            value, cascades, triggers = self.value_for_stacks(curr_value, trait_db.data.get(YAMLtags.DB_VALUES))
        if DatabaseTraitType.ONEOF in trait_db.types:
            value = self.value_for_oneof(trait_db.data.get(YAMLtags.DB_VALUES))
        if value is None:
            # TODO check for base
            value = curr_value * base_value if base_value is not None else curr_value
            if DatabaseTraitType.PERCENT in trait_db.types:
                value = "{:.0%}".format(value)
        return value, cascades, triggers

    def value_for_stacks(self, ref_value: float, stacks: list) -> tuple[Any,dict,dict]:
        """
        Generates the value for a stack.

        :param ref_value: reference value to reach with the stack.
        :param stacks: the list of stacks.
        :return: a triplet [value, cascades definitions, triggers definitions]
        """
        self.log.debug(f"stacks curr_value={ref_value}, stacks={stacks}")
        it = iter(stacks)
        stack: dict = None
        stacked_value: float = -1.0  # in case ref_value = 0
        cascades_all: dict = None
        cascades = {}
        triggers = {}
        while ref_value > stacked_value:
            stack = next(it)
            if stacked_value == -1:
                stacked_value = 0
            # check for cascade all
            if YAMLtags.DB_CASCADE_ALL_AFTER in stack:
                cascades_all = stack.get(YAMLtags.DB_CASCADE_ALL_AFTER)
            stacked_value += self.interpret_number(stack.get(YAMLtags.DB_CHANCES))
            self.log.debug(f"{ref_value} <?= {stacked_value}, {stack}")
        self.log.debug(f"end {ref_value} <= {stacked_value}, {stack}")
        actual_value = (
            stack.get(YAMLtags.DB_TEXT) if YAMLtags.DB_TEXT in stack else stack.get(YAMLtags.DB_KEY)
        )
        if YAMLtags.DB_CASCADE in stack or cascades_all:
            cascades = stack.get(YAMLtags.DB_CASCADE) if YAMLtags.DB_CASCADE in stack else cascades_all
        return actual_value, cascades, triggers

    def value_for_either(self, data: dict) -> tuple[Any,dict,dict]:
        """
        Generates the value for an either switch by selecting a possible key and generating its value.

        :param data: the trait data.
        :return: a triplet [value, cascades definitions, triggers definitions]
        """
        self.log.debug(f"value_for_either data={data}")
        all_keys: list = data.get(YAMLtags.DB_KEYS)
        default_key = data.get(YAMLtags.DB_DEFAULT_KEY)
        curr_key = default_key
        self.log.debug(f"either => {curr_key}")
        return self.generate_trait_value(DatabaseParser().create_trait_db(data.get(curr_key)))

    def value_for_oneof(self, values: list) -> Any:
        """
        Generates the value for a "oneof" trait, i.e. just select a random value.

        :param values: list of all possible values to choose from.
        :return: the selected value.
        """
        return random.choice(values)

    def interpret_number(self, value: str) -> float:
        """
        Interprets a given number.

        :param value: the number to interpret
        :return: the float value
        """
        interpreted = value
        if type(value) is str and "%" in value:
            interpreted = float(value.strip("%")) / 100
        return interpreted
