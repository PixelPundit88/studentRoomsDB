import argparse
from pathlib import Path
from typing import NamedTuple


class CLIArgs(NamedTuple):
    students: str
    rooms: str
    format: str
    output: str


class CLI:
    def __init__(self):
        self.parser = self._setup_parser()

    @staticmethod
    def _setup_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="Student Room Database Management"
        )
        parser.add_argument(
            '--students',
            required=True,
            type=str,
            help='Path to students.json file'
        )
        parser.add_argument(
            '--rooms',
            required=True,
            type=str,
            help='Path to rooms.json file'
        )
        parser.add_argument(
            '--format',
            choices=['json', 'xml'],
            default='json',
            help='Output format: json or xml (default: json)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='report',
            help='Output filename without extension (default: report)'
        )
        return parser

    def parse_args(self) -> CLIArgs:
        args = self.parser.parse_args()
        self._validate_file(args.students, "students")
        self._validate_file(args.rooms, "rooms")
        return CLIArgs(
            students=args.students,
            rooms=args.rooms,
            format=args.format,
            output=args.output
        )

    @staticmethod
    def _validate_file(filepath: str, file_type: str) -> None:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"{file_type.capitalize()} file not found: {filepath}")
        if not path.is_file():
            raise ValueError(f"{file_type.capitalize()} path is not a file: {filepath}")

    def print_help(self) -> None:
        self.parser.print_help()