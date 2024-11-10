import logging
from pathlib import Path
import yaml

from .yaml_tags import YAMLtags
from ..character_database import (
    TraitDatabase,
    MainDatabase,
    DatabaseTraitDisplayType,
)


class DatabaseParser:

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def parse(self, file: Path) -> MainDatabase | None:
        self.log.debug(f"Parsing DB {file}")
        db: MainDatabase = None
        data: dict[str, TraitDatabase] = {}
        with open(file, "r", encoding="utf-8") as db_file:
            docs = yaml.safe_load_all(db_file)
            db = MainDatabase(name=file.name, file=file)
            data: dict[str, TraitDatabase] = {}
            for doc in docs:
                next_key = next(iter(doc))
                data[next_key] = self.create_trait_db(doc.get(next_key))
            self.log.debug(data.keys())
        db.data = data
        return db

    def create_trait_db(self, trait_data: dict) -> TraitDatabase:
        trait_db = TraitDatabase(name=trait_data.get(YAMLtags.DB_NAME))
        trait_db.data = trait_data
        trait_db.types = [i_type.lower() for i_type in trait_data.get(YAMLtags.DB_TYPE)]
        trait_db.display = (
            trait_data.get(YAMLtags.DB_DISPLAY.lower())
            if YAMLtags.DB_DISPLAY in trait_data
            else DatabaseTraitDisplayType.DEFAULT
        )
        self.log.debug(f"{trait_db}")
        return trait_db
