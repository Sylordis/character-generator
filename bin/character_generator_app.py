import argparse
import logging
from pathlib import Path

from ..src.character_generator import CharacterGenerator


logger = logging.getLogger(__name__)


class ArgParser:
    """
    Class to organise and setup the different options for the software.
    """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=__name__, description="Randomly generates a character."
        )
        self.parser.add_argument("definition", help="Configuration file for character generation.")
        self.parser.add_argument(
            "dbs",
            help="Path to configuration files referenced in the configuration file.",
            metavar="files",
            nargs="+",
        )
        self.parser.add_argument(
            "-l",
            "--log",
            help="Sets the log level.",
            default="info",
            metavar="LEVEL",
            dest="loglevel",
            choices=["debug", "info", "warning", "error"],
        )
        self.parser.add_argument(
            "--debug",
            help="Sets debug mode (equivalent to '--log debug').",
            action="store_const",
            dest="loglevel",
            const="debug",
        )
        self.parser.add_argument(
            "-i",
            "--ignore-undefined",
            help="If set, ignores the undefined attributes.",
            dest="ignore_undefined",
            action="store_const",
            const=True,
        )
        self.parser.add_argument(
            "-n",
            "--number",
            help="Instructs to generate N characters.",
            metavar="N",
            dest="n_generations",
            type=int,
            default=1,
        )

    def parse(self):
        return self.parser.parse_args()


def check_files_present(files: list[Path]):
    not_exists: list[Path] = [file for file in files if not file.exists()]
    logger.debug(f"Files passed: {files}")
    logger.debug(f"Files not existing: {not_exists}")
    if len(not_exists) > 0:
        raise ValueError(f"Couldn't find following files: {not_exists}")


def main():
    args = ArgParser().parse()
    logging.basicConfig(level=getattr(logging, args.loglevel.upper(), None))
    dbs = [Path(file).resolve() for file in args.dbs]
    definition = Path(args.definition).resolve()
    check_files_present(dbs + [definition])
    CharacterGenerator(dbs, definition, args).generate(args.n_generations)
