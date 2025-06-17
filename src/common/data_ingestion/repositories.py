from sqlalchemy.orm import Session

from .records import (
    AttributeAllowableValueInAnyCategoryRecord,
    AttributeAllowableValuesApplicableInEveryCategoryRecord,
    AttributeRecord,
    CategoryAllowableValueRecord,
    CategoryAttributeRecord,
    CategoryRecord,
    DunelmCoalesceOutputRecord,
    ImageFilePathMappingRecord,
    ProductAttributeAllowableValueRecord,
    ProductAttributeGapsRecord,
    ProductAttributeValueRecord,
    ProductCategoryRecord,
    ProductRecord,
    RecommendationRecord,
    RecommendationRoundRecord,
    RichTextSourceRecord,
)


class DunelmCoalesceOutputRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, product_code: str) -> DunelmCoalesceOutputRecord | None:
        return (
            self.session.query(DunelmCoalesceOutputRecord)
            .filter_by(product_code=product_code)
            .first()
        )

    def find(self, **kwargs: str) -> list[DunelmCoalesceOutputRecord]:
        """
        Find all records matching the given column-value pairs.
        Example: find(product_code="foo", product_title="bar")
        """
        return (
            self.session.query(DunelmCoalesceOutputRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: DunelmCoalesceOutputRecord) -> None:
        self.session.add(record)
        self.session.commit()


class ImageFilePathMappingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, image_path: str) -> ImageFilePathMappingRecord | None:
        return (
            self.session.query(ImageFilePathMappingRecord)
            .filter_by(image_path=image_path)
            .first()
        )

    def find(self, **kwargs: str) -> list[ImageFilePathMappingRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(ImageFilePathMappingRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: ImageFilePathMappingRecord) -> None:
        self.session.add(record)
        self.session.commit()


class RichTextSourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, product_key: str) -> RichTextSourceRecord | None:
        return (
            self.session.query(RichTextSourceRecord)
            .filter_by(product_key=product_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[RichTextSourceRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(RichTextSourceRecord).filter_by(**kwargs).all()
        )

    def add(self, record: RichTextSourceRecord) -> None:
        self.session.add(record)
        self.session.commit()


class RecommendationRoundRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, recommendation_round_key: str
    ) -> RecommendationRoundRecord | None:
        return (
            self.session.query(RecommendationRoundRecord)
            .filter_by(recommendation_round_key=recommendation_round_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[RecommendationRoundRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(RecommendationRoundRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: RecommendationRoundRecord) -> None:
        self.session.add(record)
        self.session.commit()


class RecommendationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, product_key: str, attribute_key: str
    ) -> RecommendationRecord | None:
        return (
            self.session.query(RecommendationRecord)
            .filter_by(product_key=product_key, attribute_key=attribute_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[RecommendationRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(RecommendationRecord).filter_by(**kwargs).all()
        )

    def add(self, record: RecommendationRecord) -> None:
        self.session.add(record)
        self.session.commit()


class ProductCategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, product_key: str, category_key: str
    ) -> ProductCategoryRecord | None:
        return (
            self.session.query(ProductCategoryRecord)
            .filter_by(product_key=product_key, category_key=category_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[ProductCategoryRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(ProductCategoryRecord).filter_by(**kwargs).all()
        )

    def add(self, record: ProductCategoryRecord) -> None:
        self.session.add(record)
        self.session.commit()


class ProductAttributeValueRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, product_key: str, attribute_key: str
    ) -> ProductAttributeValueRecord | None:
        return (
            self.session.query(ProductAttributeValueRecord)
            .filter_by(product_key=product_key, attribute_key=attribute_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[ProductAttributeValueRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(ProductAttributeValueRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: ProductAttributeValueRecord) -> None:
        self.session.add(record)
        self.session.commit()


class ProductAttributeGapsRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, product_key: str, attribute_key: str
    ) -> ProductAttributeGapsRecord | None:
        return (
            self.session.query(ProductAttributeGapsRecord)
            .filter_by(product_key=product_key, attribute_key=attribute_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[ProductAttributeGapsRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(ProductAttributeGapsRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: ProductAttributeGapsRecord) -> None:
        self.session.add(record)
        self.session.commit()


class ProductAttributeAllowableValueRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, product_key: str, attribute_key: str
    ) -> ProductAttributeAllowableValueRecord | None:
        return (
            self.session.query(ProductAttributeAllowableValueRecord)
            .filter_by(product_key=product_key, attribute_key=attribute_key)
            .first()
        )

    def find(
        self, **kwargs: str
    ) -> list[ProductAttributeAllowableValueRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(ProductAttributeAllowableValueRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: ProductAttributeAllowableValueRecord) -> None:
        self.session.add(record)
        self.session.commit()


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, product_key: str) -> ProductRecord | None:
        return (
            self.session.query(ProductRecord)
            .filter_by(product_key=product_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[ProductRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return self.session.query(ProductRecord).filter_by(**kwargs).all()

    def add(self, record: ProductRecord) -> None:
        self.session.add(record)
        self.session.commit()


class CategoryAttributeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, category_attribute_key: str
    ) -> CategoryAttributeRecord | None:
        return (
            self.session.query(CategoryAttributeRecord)
            .filter_by(category_attribute_key=category_attribute_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[CategoryAttributeRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(CategoryAttributeRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: CategoryAttributeRecord) -> None:
        self.session.add(record)
        self.session.commit()


class CategoryAllowableValueRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, category_attribute_key: str
    ) -> CategoryAllowableValueRecord | None:
        return (
            self.session.query(CategoryAllowableValueRecord)
            .filter_by(category_attribute_key=category_attribute_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[CategoryAllowableValueRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(CategoryAllowableValueRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: CategoryAllowableValueRecord) -> None:
        self.session.add(record)
        self.session.commit()


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, category_key: str) -> CategoryRecord | None:
        return (
            self.session.query(CategoryRecord)
            .filter_by(category_key=category_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[CategoryRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return self.session.query(CategoryRecord).filter_by(**kwargs).all()

    def add(self, record: CategoryRecord) -> None:
        self.session.add(record)
        self.session.commit()


class AttributeAllowableValuesApplicableInEveryCategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, attribute_key: str
    ) -> AttributeAllowableValuesApplicableInEveryCategoryRecord | None:
        return (
            self.session.query(
                AttributeAllowableValuesApplicableInEveryCategoryRecord
            )
            .filter_by(attribute_key=attribute_key)
            .first()
        )

    def find(
        self, **kwargs: str
    ) -> list[AttributeAllowableValuesApplicableInEveryCategoryRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(
                AttributeAllowableValuesApplicableInEveryCategoryRecord
            )
            .filter_by(**kwargs)
            .all()
        )

    def add(
        self, record: AttributeAllowableValuesApplicableInEveryCategoryRecord
    ) -> None:
        self.session.add(record)
        self.session.commit()


class AttributeAllowableValueInAnyCategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(
        self, attribute_key: str
    ) -> AttributeAllowableValueInAnyCategoryRecord | None:
        return (
            self.session.query(AttributeAllowableValueInAnyCategoryRecord)
            .filter_by(attribute_key=attribute_key)
            .first()
        )

    def find(
        self, **kwargs: str
    ) -> list[AttributeAllowableValueInAnyCategoryRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return (
            self.session.query(AttributeAllowableValueInAnyCategoryRecord)
            .filter_by(**kwargs)
            .all()
        )

    def add(self, record: AttributeAllowableValueInAnyCategoryRecord) -> None:
        self.session.add(record)
        self.session.commit()


class AttributeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get(self, attribute_key: str) -> AttributeRecord | None:
        return (
            self.session.query(AttributeRecord)
            .filter_by(attribute_key=attribute_key)
            .first()
        )

    def find(self, **kwargs: str) -> list[AttributeRecord]:
        """
        Find all records matching the given column-value pairs.
        """
        return self.session.query(AttributeRecord).filter_by(**kwargs).all()

    def add(self, record: AttributeRecord) -> None:
        self.session.add(record)
        self.session.commit()
