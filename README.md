# MBTA Transit Data Pipeline

A data engineering project built around Massachusetts Bay Transportation Authority (MBTA) transit data.

The goal of this project is to build a near-real-time data pipeline that ingests, stores, and analyzes MBTA transit data, culminating in a transit reliability dashboard. The project is designed to explore real-world data engineering concepts including REST API ingestion, GTFS-Realtime (protobuf) ingestion, incremental processing, data partitioning, orchestration, data quality, and analytical data modeling.

A future phase will incorporate weather data and machine learning to investigate whether weather conditions can be used to explain or predict transit delays.

## Project Thesis

Build a dashboard showing near-real-time MBTA vehicle positions and reliability metrics (on-time performance, delay trends), refreshed on the order of tens of seconds — not literal streaming, but frequent enough that it reads as "live" for a transit rider.

This is deliberately split into two paths with different tools and different jobs:

* **Hot path** — a lightweight, frequently-polled ingestion of GTFS-Realtime data (vehicle positions, trip updates, alerts), producing a small "current state" view. Simple by design; no orchestration overhead.
* **Cold path** — periodic batch ingestion of reference data (routes, stops, schedules) and archival of historical vehicle/trip data into partitioned Parquet, transformed via dbt/DuckDB, orchestrated by Airflow. This is where most of the data engineering learning happens.

The dashboard reads live state from the hot path and historical/aggregated metrics from the cold path.

## Project Goals

* Ingest MBTA reference data (routes, stops, schedules) from the MBTA REST API (JSON)
* Ingest MBTA real-time data (vehicle positions, trip updates, alerts) from GTFS-Realtime (protobuf) feeds
* Store raw data in an efficient, queryable format, partitioned by time
* Maintain a separate "current state" view distinct from append-only history
* Build reliable, incremental batch ingestion orchestrated by Airflow
* Handle API failures, retries, and malformed data
* Transform raw data into analytical datasets (on-time performance, delay trends)
* Build a near-real-time transit reliability dashboard
* Incorporate weather data for additional analysis
* Develop a machine learning pipeline for transit delay prediction

## Planned Architecture

```text
                 MBTA REST API (JSON)              MBTA GTFS-Realtime (protobuf)
                 routes / stops / schedules          vehicle positions / trip updates / alerts
                          │                                        │
                          ▼                                        ▼
                  Cold path (batch,                        Hot path (frequent
                  Airflow-orchestrated)                     poll, no orchestration)
                          │                                        │
                          ▼                                        ▼
                  Historical Parquet                        Current-state store
                  (partitioned)                              (overwritten each poll)
                          │                                        │
                          ▼                                        │
                       DuckDB                                      │
                          │                                        │
                         dbt                                        │
                          │                                        │
                 ┌────────┴────────┐                                │
                 ▼                 ▼                                │
            Reliability       ML Features                           │
            Metrics               │                                 │
                 │                 ▼                                │
                 │            ML Model                              │
                 └────────┬────────┘                                │
                          ▼                                         │
                      Dashboard  ◄───────────────────────────────────┘
```

## Technology Stack

### Phase 1 — Data Ingestion

* Python
* Requests (MBTA REST API — reference data)
* GTFS-Realtime bindings / Protocol Buffers (real-time feeds — vehicle positions, trip updates, alerts)
* PyArrow / Parquet
* pytest

### Planned

* DuckDB
* dbt
* Apache Airflow (cold path orchestration only)
* Streamlit
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
* [x] MBTA REST API ingestion (routes)
* [ ] MBTA REST API ingestion (stops, schedules)
* [ ] GTFS-Realtime ingestion (vehicle positions)
* [ ] GTFS-Realtime ingestion (trip updates, alerts)
* [ ] Current-state storage (hot path)
* [ ] Historical Parquet storage (cold path, partitioned)
* [ ] Incremental ingestion
* [ ] Error handling and retries
* [ ] API key / secrets management

### Phase 2 — Data Warehouse & Transformation

**Planned**

* [ ] Airflow orchestration (cold path)
* [ ] DuckDB
* [ ] dbt
* [ ] Data quality tests
* [ ] On-time performance / reliability data model

### Phase 3 — Visualization

**Planned**

* [ ] Live vehicle-position view (hot path)
* [ ] Transit reliability metrics (cold path)
* [ ] Streamlit dashboard

### Phase 4 — Weather & Machine Learning

**Planned, stretch goal — revisit after Phases 1–3 are stable and running unattended for several weeks**

* [ ] Weather data ingestion
* [ ] Weather/transit data integration
* [ ] Feature engineering
* [ ] Delay prediction model
* [ ] Model evaluation
* [ ] ML predictions in dashboard

## Learning Objectives

This project is primarily intended as a hands-on exploration of modern data engineering practices using publicly available transit data.

Key areas of focus include:

* REST APIs and JSON
* GTFS-Realtime and Protocol Buffers
* Incremental data processing
* Data partitioning and "current state" vs. append-only history design
* Parquet
* SQL and analytical data modeling
* Pipeline orchestration (batch, not streaming)
* Data quality and testing
* Machine learning pipelines
* CI/CD