# MBTA Data Pipeline — Copilot Instructions

## Project

This is a personal data engineering project using MBTA transit data.

The goal is to build an end-to-end ETL pipeline that:
- Ingests MBTA transit data
- Stores raw and processed data as Parquet
- Eventually uses DuckDB and dbt for transformation
- Provides a dashboard for transit analysis
- May eventually incorporate weather data and machine learning

## Technology

Current:
- Python
- Requests
- PyArrow
- Protobuf
- GTFS-Realtime bindings
- pytest

Planned:
- DuckDB
- dbt
- Airflow
- Streamlit
- scikit-learn
- Docker

## Architecture

The intended pipeline is:

MBTA API → Python ingestion → Parquet → DuckDB → transformations → dashboard

A future ML pipeline may combine MBTA transit data with weather data to predict transit delays.

## Development Guidelines

- Prefer simple, readable Python.
- Use type hints.
- Write functions that are easy to test.
- Handle API failures explicitly.
- HTTP requests should have timeouts.
- Do not hard-code API responses or generated data.
- Keep ingestion, transformation, and storage logic separated.
- Do not add dependencies without explaining why they are needed.
- Do not modify project architecture without discussing the change first.
- Prefer incremental, understandable implementations over complex abstractions.