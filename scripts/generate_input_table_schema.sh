#!/bin/bash

set -e

python -m src.common.data_ingestion.csv_schema_generator schema/02_input_tables.sql