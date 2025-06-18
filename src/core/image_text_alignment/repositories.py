import logging
import os

from src.common.logging import setup_logging
from src.core.data_ingestion.dtos import DunelmCoalesceOutputDTO
from src.core.data_ingestion.repositories import (
    AttributeRepository,
    DunelmCoalesceOutputRepository,
    ProductAttributeValueRepository,
    ProductRepository,
)
from src.core.image_text_alignment.records import (
    Categories,
    ImageLocalPaths,
    Prices,
    ProductOverviewRecord,
)

logger = logging.getLogger(__name__)
setup_logging()


class ProductOverviewRepository:
    def __init__(
        self,
        product_repo: ProductRepository,
        coalesce_repo: DunelmCoalesceOutputRepository,
        pav_repo: ProductAttributeValueRepository,
        attr_repo: AttributeRepository,
    ) -> None:
        self.product_repo = product_repo
        self.coalesce_repo = coalesce_repo
        self.pav_repo = pav_repo
        self.attr_repo = attr_repo

    def _get_image_local_path(
        self, coalesce: DunelmCoalesceOutputDTO, i: int
    ) -> str | None:
        url = getattr(coalesce, f"image_url_{i}", None)
        if url:
            filename = os.path.basename(url.split("?")[0])
            return f"data/image/{filename}"
        return None

    def get_product_overview(
        self, product_key: str
    ) -> ProductOverviewRecord | None:
        product_orm = self.product_repo.get(product_key)
        if not product_orm:
            logger.warning(
                f"No product record found for product_key={product_key}"
            )
            return None

        product = product_orm.to_dto()
        if product.system_name is None:
            logger.warning(
                f"Product system_name is None for product_key={product_key}"
            )
            return None

        # TODO: This is a hack to get the coalesce record for the product.
        # system_name is the URL this time, not the EAN.
        coalesce_orm = self.coalesce_repo.get_by_product_url(
            product.system_name
        )
        if not coalesce_orm:
            logger.warning(
                f"No coalesce record found for product_key={product_key}, "
                f"system_name={product.system_name}"
            )
            return None
        coalesce = coalesce_orm.to_dto()

        attr_values = self.pav_repo.get_by_product_key(product_key)
        attribute_values = []
        for av in attr_values:
            av_dto = av.to_dto()
            attr = self.attr_repo.get(str(av.attribute_key))
            attr_name = attr.to_dto().friendly_name if attr else None
            attribute_values.append(
                {
                    "attribute_key": str(av_dto.attribute_key),
                    "attribute_name": attr_name,
                    "value": av_dto.value,
                    "unit": av_dto.unit,
                    "minimum_value": av_dto.minimum_value,
                    "minimum_unit": av_dto.minimum_unit,
                    "maximum_value": av_dto.maximum_value,
                    "maximum_unit": av_dto.maximum_unit,
                    "range_qualifier_enum": av_dto.range_qualifier_enum,
                }
            )

        image_local_paths = ImageLocalPaths(
            **{
                f"image_local_path_{i}": self._get_image_local_path(
                    coalesce, i
                )
                for i in range(1, 11)
            }
        )

        categories = Categories(
            **{
                f"category_{i}": getattr(coalesce, f"category_{i}", None)
                for i in range(4)
            }
        )

        prices = Prices(
            now_price=getattr(coalesce, "now_price", None),
            was_price=getattr(coalesce, "was_price", None),
            save_message=getattr(coalesce, "save_message", None),
        )

        return ProductOverviewRecord(
            product_key=product.product_key,
            system_name=product.system_name,
            friendly_name=product.friendly_name,
            product_code=getattr(coalesce, "product_code", None),
            product_title=getattr(coalesce, "product_title", None),
            product_url=getattr(coalesce, "product_url", None),
            categories=categories,
            description_text=getattr(coalesce, "description_text", None),
            specification_text=getattr(coalesce, "specification_text", None),
            specification_attributes_xml=getattr(
                coalesce, "specification_attributes_xml", None
            ),
            image_local_paths=image_local_paths,
            prices=prices,
            on_promotion=getattr(coalesce, "on_promotion", None),
            review_count=getattr(coalesce, "review_count", None),
            review_rating=getattr(coalesce, "review_rating", None),
            attribute_values=attribute_values,
        )
