import csv
import logging
from pathlib import Path
from typing import Any, Callable, Iterator

from tqdm import tqdm

from src.common.file_readers.types import ProcessingResult

logger = logging.getLogger(__name__)


def iter_csv_batches(
    file_path: str | Path,
    batch_size: int = 1000,
    column_mapping: dict[str, str] | None = None,
    row_limit: int | None = None,
    encoding: str = "utf-8-sig",
) -> Iterator[list[dict[str, Any]]]:
    file_path = Path(file_path)
    with file_path.open(newline="", encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        batch: list[dict[str, Any]] = []
        total = 0
        for line in reader:
            if column_mapping:
                mapped_line = {
                    param: line[col] for col, param in column_mapping.items()
                }
            else:
                mapped_line = line
            batch.append(mapped_line)
            total += 1
            if len(batch) == batch_size:
                yield batch
                batch = []
            if row_limit and total >= row_limit:
                break
        if batch:
            yield batch


def process_csv_file(
    file_path: Path,
    create_func: Callable[..., Any],
    batch_size: int = 1000,
    column_mapping: dict[str, str] | None = None,
    row_limit: int | None = None,
) -> ProcessingResult:
    rows_processed = 0
    rows_skipped = 0
    total_processed = 0

    logger.debug(f"Processing {file_path} (limit: {row_limit or 'none'})")

    pbar = tqdm(
        desc=file_path.name,
        unit="rows",
        leave=True,
        bar_format=(
            "{l_bar}{bar}| {n_fmt}/{total_fmt} "
            "[{elapsed}<{remaining}, {rate_fmt}]"
        ),
        dynamic_ncols=True,
        total=None,
    )

    for batch in iter_csv_batches(
        file_path=file_path,
        batch_size=batch_size,
        column_mapping=column_mapping,
        row_limit=row_limit,
    ):
        for record in batch:
            if row_limit and total_processed >= row_limit:
                break
            result = create_func(**record)
            if result is None:
                rows_skipped += 1
            else:
                rows_processed += 1
            total_processed += 1
            pbar.update(1)
        if row_limit and total_processed >= row_limit:
            break

    pbar.close()
    logger.info(
        f"Processed {rows_processed} rows from {file_path.name} "
        f"({rows_skipped} duplicates skipped)"
    )

    return ProcessingResult(
        rows_processed=rows_processed,
        rows_skipped=rows_skipped,
        total_processed=total_processed,
    )
