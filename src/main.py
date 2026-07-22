import sys
from contextlib import contextmanager
from pathlib import Path
from dotenv import load_dotenv

from src.config import DatabaseConfig
from src.db_manager import DatabaseConnection
from src.loader import DataLoader
from src.queries import QueryService
from src.exporter import ExporterFactory
from src.cli import CLI


@contextmanager
def database_connection():
    db = DatabaseConnection(DatabaseConfig())
    try:
        db.connect()
        yield db
    finally:
        db.close()


def main() -> int:
    load_dotenv()

    try:
        args = CLI().parse_args()

        with database_connection() as db:
            loader = DataLoader(db)
            rooms_count, students_count = loader.load_all(args.rooms, args.students)
            print(f"Loaded {rooms_count} rooms and {students_count} students")

            query_service = QueryService(db)
            results = query_service.run_all_queries()

            exporter = ExporterFactory.get_exporter(args.format)
            output = exporter.export(results)

            output_dir = Path("output")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"{args.output}.{args.format}"
            output_path.write_text(output, encoding='utf-8')
            print(f"Results written to {output_path}")

        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Database connection error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())