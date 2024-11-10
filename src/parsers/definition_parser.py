from pathlib import Path
import yaml

from ..character_definition import CharacterDefinition, CharacterDefinitionEntry
from .yaml_tags import YAMLtags


class DefinitionParser:

    def parse(self, definition_file: Path) -> CharacterDefinition | None:
        definition: CharacterDefinition = None
        data = {}
        with open(definition_file, 'r') as file:
            definition = CharacterDefinition()
            data = yaml.safe_load(file)
            if YAMLtags.CHARACTER_DEFINITION_ROOT in data and YAMLtags.CHARACTER_DEFINITION in data[YAMLtags.CHARACTER_DEFINITION_ROOT]:
                yaml_def: dict = data.get(YAMLtags.CHARACTER_DEFINITION_ROOT).get(YAMLtags.CHARACTER_DEFINITION)
                for yaml_entry in yaml_def:
                    db = yaml_entry.get(YAMLtags.CHARACTER_DEFINITION_FROM)
                    for entry in yaml_entry.get(YAMLtags.CHARACTER_DEFINITION_VALUES):
                        definition.entries.append(CharacterDefinitionEntry(db, entry))
            else:
                raise ValueError(f"Parsing error, {definition_file} is not formed properly.")
        return definition
