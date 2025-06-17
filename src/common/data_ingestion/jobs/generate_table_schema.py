import csv
import re
import sys
from pathlib import Path

import openpyxl

CSV_DIR = Path("data/csv")
DEFAULT_OUTPUT_SQL = Path("schemas/02_csv_input_tables.sql")


def to_snake_case(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace(" ", "_").replace("-", "_").lower()


def get_csv_header(file_path: Path) -> list[str]:
    with file_path.open("r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        for row in reader:
            if any(cell.strip() for cell in row):
                return row
    return []


def get_xlsx_header(file_path: Path) -> list[str]:
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = getattr(wb, "active", None)
    if ws is None:
        raise ValueError(f"Could not find active worksheet in {file_path}")
    for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
        return [str(cell) if cell is not None else "" for cell in row]
    return []


def generate_schema(output_sql: Path = DEFAULT_OUTPUT_SQL) -> None:
    statements = []
    for file in sorted(CSV_DIR.iterdir()):
        if file.suffix.lower() == ".csv":
            header = get_csv_header(file)
        elif file.suffix.lower() == ".xlsx":
            header = get_xlsx_header(file)
        else:
            continue
        if not header:
            continue
        table_name = to_snake_case(file.stem)
        columns = [
            f"    {to_snake_case(col)} TEXT" for col in header if col.strip()
        ]
        statement = (
            f"CREATE TABLE {table_name} (\n" + ",\n".join(columns) + "\n);\n"
        )
        statements.append(statement)
    output_sql.parent.mkdir(parents=True, exist_ok=True)
    with output_sql.open("w", encoding="utf-8") as f:
        f.write("\n".join(statements))
    print(f"Wrote schema for {len(statements)} tables to {output_sql}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_path = Path(sys.argv[1])
    else:
        output_path = DEFAULT_OUTPUT_SQL
    generate_schema(output_path)
