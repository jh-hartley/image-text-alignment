#!/bin/bash

set -e

python -m src.common.data_ingestion.ingest_csvs data/csv/DunelmCoalesce_Output_20250124.csv dunelm_coalesce_output
python -m src.common.data_ingestion.ingest_csvs data/csv/imageFilePathMapping.csv image_file_path_mapping
python -m src.common.data_ingestion.ingest_csvs data/csv/RichTextSource.csv rich_text_source
python -m src.common.data_ingestion.ingest_csvs data/csv/RecommendationRound.csv recommendation_round
python -m src.common.data_ingestion.ingest_csvs data/csv/Recommendation.csv recommendation
python -m src.common.data_ingestion.ingest_csvs data/csv/ProductCategory.csv product_category
python -m src.common.data_ingestion.ingest_csvs data/csv/ProductAttributeValue.csv product_attribute_value
python -m src.common.data_ingestion.ingest_csvs data/csv/ProductAttributeGaps.csv product_attribute_gaps
python -m src.common.data_ingestion.ingest_csvs data/csv/ProductAttributeAllowableValue.csv product_attribute_allowable_value
python -m src.common.data_ingestion.ingest_csvs data/csv/Product.csv product
python -m src.common.data_ingestion.ingest_csvs data/csv/CategoryAttribute.csv category_attribute
python -m src.common.data_ingestion.ingest_csvs data/csv/CategoryAllowableValue.csv category_allowable_value
python -m src.common.data_ingestion.ingest_csvs data/csv/Category.csv category
python -m src.common.data_ingestion.ingest_csvs data/csv/AttributeAllowableValuesApplicableInEveryCategory.csv attribute_allowable_values_applicable_in_every_category
python -m src.common.data_ingestion.ingest_csvs data/csv/AttributeAllowableValueInAnyCategory.csv attribute_allowable_value_in_any_category
python -m src.common.data_ingestion.ingest_csvs data/csv/Attribute.csv attribute
