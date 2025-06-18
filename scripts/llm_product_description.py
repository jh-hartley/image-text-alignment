import sys
from pathlib import Path

from sqlalchemy.orm import Session

from src.common.db.engine import engine
from src.core.image_text_alignment.repositories import (
    ProductOverviewRepository,
)

OUTPUT_DIR = Path(__file__).parent / "llm_test_output"


def main(product_key: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    with Session(engine) as session:
        repo = ProductOverviewRepository(session)
        overview = repo.get_product_overview(product_key)
        if overview is None:
            print(f"No product overview found for product_key: {product_key}")
            sys.exit(1)
        llm_str = overview.to_llm_string()
        output_path = OUTPUT_DIR / f"{product_key}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(llm_str)
        print(f"Saved product description to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python llm_product_description.py <PRODUCT_KEY>")
        sys.exit(1)
    main(sys.argv[1])
