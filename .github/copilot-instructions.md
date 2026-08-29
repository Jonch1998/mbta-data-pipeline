# MBTA Data Pipeline — Copilot Instructions

## Project

This is a personal data engineering project using MBTA transit data.

The goal is to build a near-real-time pipeline that:
- Ingests MBTA reference data (routes, stops, schedules) from the MBTA REST API (JSON)
- Ingests MBTA real-time data (vehicle positions, trip updates, alerts) from GTFS-Realtime (protobuf) feeds
- Stores raw and processed data as Parquet
- Eventually uses DuckDB and dbt for transformation
- Provides a dashboard for transit analysis (live vehicle positions + reliability metrics)
- May eventually incorporate weather data and machine learning

## Architecture: Hot Path / Cold Path

This project deliberately splits ingestion into two paths — do not merge them or route both through the same orchestration:

- **Hot path**: frequent (tens-of-seconds) polling of GTFS-Realtime feeds (vehicle positions, trip updates, alerts), producing a small "current state" view that the dashboard reads directly. No Airflow, no heavy orchestration — keep this simple.
- **Cold path**: periodic (hourly/daily) batch ingestion of reference data (routes, stops, schedules) and archival of historical data into partitioned Parquet, transformed via dbt/DuckDB, orchestrated by Airflow.

Airflow is for the cold path only. Do not design tasks that assume Airflow will run sub-minute polling.

## Technology

Current:
- Python
- Requests (MBTA REST API — reference data)
- PyArrow
- Protobuf
- GTFS-Realtime bindings (real-time feeds)
- pytest

Planned:
- DuckDB
- dbt
- Airflow (cold path orchestration only)
- Streamlit
- scikit-learn
- Docker

## Architecture

The intended pipeline is:

MBTA REST API (JSON, reference data) + MBTA GTFS-Realtime (protobuf, real-time data)
→ Python ingestion (hot path + cold path)
→ Current-state store (hot) / Raw Parquet (cold, partitioned)
→ DuckDB → dbt transformations → dashboard

A future ML pipeline may combine MBTA transit data with weather data to predict transit delays.

## Storage Design

- Keep "current state" (latest vehicle positions/predictions) separate from append-only historical data. Current state is small and overwritten each poll; history is partitioned (e.g., by date) and never overwritten.
- Do not conflate the two into a single growing table meant for both live lookups and historical analysis.

## Secrets & Configuration

- MBTA API keys must not be hard-coded or committed. Load them from environment variables or a local `.env` file excluded via `.gitignore`.
- GTFS-Realtime feeds are typically public and keyless; the JSON REST API benefits from a registered key for higher rate limits — do not assume keyless access is sufficient once polling frequency increases.

## Development Guidelines

- Prefer simple, readable Python.
- Use type hints.
- Write functions that are easy to test.
- Handle API failures explicitly.
- HTTP requests should have timeouts.
- Do not hard-code API responses or generated data in production ingestion code. Recorded/fixture responses are expected and fine for tests.
- Keep ingestion, transformation, and storage logic separated.
- Keep hot-path and cold-path ingestion code separated — do not let live-polling code depend on batch/orchestration modules or vice versa.
- Do not add dependencies without explaining why they are needed.
- Do not modify project architecture without discussing the change first.
- Prefer incremental, understandable implementations over complex abstractions.