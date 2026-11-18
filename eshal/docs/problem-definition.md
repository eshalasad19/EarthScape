# Problem Definition

## Background
EarthScape Climate Agency collects large volumes of climate data: weather station records, environmental sensor readings (e.g. CO2, humidity) and satellite imagery. The data arrives in different formats, is growing continuously and is hard to analyze with traditional tools.

## Problem
The agency needs a system that can:
- Store large, mixed climate datasets (historical and incoming data) reliably
- Process the data at scale to find patterns, anomalies and correlations, and handle missing or incomplete data
- Let analysts query the data quickly
- Predict climate trends and detect anomalies with machine learning
- Notify stakeholders when unusual values appear
- Present results through interactive dashboards
- Control who can access what (different user roles), protect data and keep backups
- Collect user feedback and support requests

## Objective
Build a Big Data solution using Hadoop/HDFS for storage and MapReduce for processing, Impala for fast querying, MongoDB for users, readings, alerts and feedback, Jupyter and RStudio for machine learning, and Tableau for dashboards.

## Scope
**In scope:** data ingestion (historical and simulated real-time), HDFS storage and partitioning, MapReduce analysis, Impala queries, ML models (trend prediction, anomaly detection, correlation), alerts, Tableau dashboards, role-based access, backup, monitoring, feedback and support, documentation.

**Out of scope:** tools and technologies outside the project's approved stack.

## Users
- **Admin:** manages data, users and system
- **Analyst:** queries data, views dashboards and alerts, submits feedback

## Success criteria
- Data flows end to end: ingestion -> HDFS -> MapReduce -> Impala/ML -> dashboards
- Analysts can only read; admins can manage
- Anomalies produce alerts
- System is documented, backed up and monitored