import logging
from pathlib import Path
import yaml

from ..character_database import CharacterDatabase


class DataBaseParser:

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
    
    def parse(self, file: Path) -> CharacterDatabase | None:
        self.log.debug(f"Parsing DB {file}")
        db: CharacterDatabase = None
        with open(file, 'r', encoding='utf-8') as db_file:
            docs = yaml.safe_load_all(db_file)
            data = {}
            for doc in docs:
                next_key = next(iter(doc))
                data[next_key] = doc.get(next_key)
            self.log.debug(data.keys())
            db = CharacterDatabase(data=data)
        return db
