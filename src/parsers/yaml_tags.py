from enum import StrEnum


class YAMLtags(StrEnum):
    """
    Definition of YAML tags.
    """

    CHARACTER_DEFINITION_ROOT = "character"
    CHARACTER_DEFINITION = "definition"
    CHARACTER_DEFINITION_FROM = "from"
    CHARACTER_DEFINITION_VALUES = "values"

    DB_CASCADE = "cascade"
    DB_CASCADE_ALL_AFTER = "cascade_all_after"
    DB_CHANCES = "chances"
    DB_DISPLAY = "display"
    DB_KEY = "key"
    DB_KEYS = "keys"
    DB_DEFAULT_KEY = "default_key"
    DB_NAME = "name"
    DB_TEXT = "text"
    DB_TRIGGER = "trigger"
    DB_TRIGGER_ALL_AFTER = "trigger_all_after"
    DB_TYPE = "type"
    DB_VALUES = "values"
