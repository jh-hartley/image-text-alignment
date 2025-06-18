import asyncio
import shutil
import sys
from pathlib import Path

from src.common.db.session import SessionLocal
from src.common.llm import Llm
from src.core.image_text_alignment.repositories import (
    ProductOverviewRepository,
)
from src.core.image_text_alignment.service import ImageTextAlignmentService

OUTPUT_DIR = Path(__file__).parent / "llm_output"


def clear_output_dir():
    if OUTPUT_DIR.exists():
        for item in OUTPUT_DIR.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    else:
        OUTPUT_DIR.mkdir()


def main(product_key: str):
    async def run():
        clear_output_dir()
        with SessionLocal() as session:
            repo = ProductOverviewRepository(session)
            llm = Llm()
            service = ImageTextAlignmentService(
                product_overview_repo=repo, llm=llm
            )
            results = await service.check_images_for_products([product_key])
            # Save results to file
            output_txt = OUTPUT_DIR / f"{product_key}.txt"
            with open(output_txt, "w", encoding="utf-8") as f:
                for result in results:
                    f.write(f"Product Key: {result.product_key}\n")
                    f.write(f"Is Mismatch: {result.is_mismatch}\n")
                    f.write(f"Justification: {result.justification}\n\n")
            print(f"Results saved to {output_txt}")
            # Copy the first image used (if any)
            product = repo.get_product_overview(product_key)
            if product:
                image_paths = [
                    v
                    for v in product.image_local_paths.model_dump().values()
                    if v
                ]
                if image_paths:
                    image_path = Path(image_paths[0])
                    if image_path.exists():
                        dest_path = OUTPUT_DIR / image_path.name
                        shutil.copy(image_path, dest_path)
                        print(f"Copied image to {dest_path}")
                    else:
                        print(f"Image file not found: {image_path}")
                else:
                    print("No image paths found for product.")
            else:
                print("No product overview found.")

    asyncio.run(run())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_image_text_alignment_llm.py <PRODUCT_KEY>")
        sys.exit(1)
    product_key = sys.argv[1]
    main(product_key)
