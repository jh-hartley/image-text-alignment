#!/bin/bash

set -e

python -m src.core.data_ingestion.jobs.generate_table_schema schema/02_input_tables.sql