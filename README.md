# MBTA Transit Data Pipeline

A data engineering project built around Massachusetts Bay Transportation Authority (MBTA) transit data.

The goal of this project is to build an end-to-end data pipeline that collects, processes, stores, and analyzes MBTA transit data. The project is designed to explore real-world data engineering concepts including API ingestion, GTFS and GTFS-Realtime data, incremental processing, data partitioning, data quality, orchestration, and analytical data modeling.

A future phase will incorporate weather data and machine learning to investigate whether weather conditions can be used to explain or predict transit delays.

## Project Goals

* Ingest MBTA transit data from public APIs
* Work with both static GTFS and GTFS-Realtime data
* Store raw data in an efficient, queryable format
* Build reliable incremental ingestion pipelines
* Handle API failures, retries, and malformed data
* Transform raw data into analytical datasets
* Build a transit reliability dashboard
* Incorporate weather data for additional analysis
* Develop a machine learning pipeline for transit delay prediction

## Planned Architecture

```text
                    MBTA API
                       │
                       ▼
                 Python Ingestion
                       │
                       ▼
                  Raw Parquet
                       │
                       ▼
                    DuckDB
                       │
                       ▼
                      dbt
                       │
                 ┌─────┴─────┐
                 ▼           ▼
             Analytics    ML Features
                 │           │
                 ▼           ▼
             Dashboard    ML Model
```

Apache Airflow will eventually be used to orchestrate the pipeline.

## Technology Stack

### Phase 1 — Data Ingestion

* Python
* Requests
* PyArrow
* GTFS / GTFS-Realtime
* Protocol Buffers
* Parquet

### Planned

* DuckDB
* dbt
* Apache Airflow
* Streamlit
* pytest
* GitHub Actions
* scikit-learn
* Docker

## Project Status

### Phase 1 — Data Ingestion

**In progress**

* [x] Development environment
* [x] Git repository
* [x] GitHub repository
* [x] Python virtual environment
* [x] Initial project structure
* [ ] MBTA REST API ingestion
* [ ] GTFS ingestion
* [ ] GTFS-Realtime ingestion
* [ ] Parquet storage
* [ ] Incremental ingestion
* [ ] Error handling and retries
* [ ] Data partitioning

### Phase 2 — Data Warehouse & Transformation

**Planned**

* [ ] DuckDB
* [ ] dbt
* [ ] Data quality tests
* [ ] Analytical data model

### Phase 3 — Visualization

**Planned**

* [ ] Transit reliability metrics
* [ ] Streamlit dashboard

### Phase 4 — Weather & Machine Learning

**Planned**

* [ ] Weather data ingestion
* [ ] Weather/transit data integration
* [ ] Feature engineering
* [ ] Delay prediction model
* [ ] Model evaluation
* [ ] ML predictions in dashboard

## Learning Objectives

This project is primarily intended as a hands-on exploration of modern data engineering practices using publicly available transit data.

Key areas of focus include:

* REST APIs
* GTFS
* GTFS-Realtime
* Protocol Buffers
* ETL/ELT
* Incremental data processing
* Data partitioning
* Parquet
* SQL
* Data modeling
* Pipeline orchestration
* Data quality and testing
* Machine learning pipelines
* CI/CD
