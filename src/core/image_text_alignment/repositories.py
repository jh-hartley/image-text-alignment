import logging
import os
import re

from sqlalchemy.orm import Session

from src.common.logging import setup_logging
from src.core.data_ingestion.repositories import (
    AttributeRepository,
    DunelmCoalesceOutputRepository,
    ImageFilePathMappingRepository,
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
    def __init__(self, session: Session) -> None:
        self.product_repo = ProductRepository(session)
        self.coalesce_repo = DunelmCoalesceOutputRepository(session)
        self.pav_repo = ProductAttributeValueRepository(session)
        self.attr_repo = AttributeRepository(session)
        self.image_path_repo = ImageFilePathMappingRepository(session)

    @staticmethod
    def _map_image_url_to_local_path(
        image_url: str, image_path_repo: ImageFilePathMappingRepository
    ) -> str | None:
        """
        Trim the image_url at the file extension (jpg, jpeg, png, etc.)
        and map the trimmed url to the local path. Bespoke to the current
        file structure.
        """
        if image_url:
            match = re.search(
                r"\.(jpg|jpeg|png|webp|gif)", image_url, re.IGNORECASE
            )
            if match:
                ext = match.group(0)
                idx = image_url.lower().find(ext) + len(ext)
                trimmed_url = image_url[:idx]
            else:
                trimmed_url = image_url
            mapping = image_path_repo.find(image_url=trimmed_url)
            if mapping:
                local_path = mapping[0].to_dto().image_path.replace("\\", "/")
                filename = os.path.basename(local_path)
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

        image_local_paths_dict = {}
        for i in range(1, 11):
            image_url = getattr(coalesce, f"image_url_{i}", None)
            if image_url is not None:
                local_path = self._map_image_url_to_local_path(
                    image_url, self.image_path_repo
                )
            else:
                local_path = None
                logger.debug(f"No image_url_{i} present.")
            image_local_paths_dict[f"image_local_path_{i}"] = local_path
        image_local_paths = ImageLocalPaths(**image_local_paths_dict)

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
