# Data-Prepper, OpenSearch and OpenSearch Dashboard


This document outlines the process and steps involved in deploying Data-Prepper, OpenSearch and OpenSearch Dashboard in the Kubernetes Cluster.

## Overview
### Trace Analytics
Data-Prepper pipeline can be customized to ingest and transform the data for use in OpenSearch. Upon transformation, the trace data can be visualized for use with the Observability plugin inside of OpenSearch DashBoards. Trace data provides visibility in the the instrumented application's performance and helps user gain more information about individual traces.

# **letak gambar trace analytic kat sini**

To monitor trace analytics, the following components need to be prepared in the environment:

- Add **instrumentation** to the application so it can generate telemetry data and send it to OpenTelemetry collector.
- Run OpenTelemetry collector and configure it to export trace data to Data-Prepper.
- Deploy Data-Prepper as the ingestion collector for OpenSearch. Configure it to send the enriched trace data to the OpenSearch cluster.
- Use OpenSearch dashboards to visualize and detect problems in the distributed application.

Three pipelines in DataPrepper would be needed:

- Entry pipeline
- Raw trace pipeline
- Service map pipeline

The OpenTelemetry source accepts trace data from the OpenTelemetry Collector. The source follows the OpenTelemetry Protocol. There are three processors needed for the trace analytics feature:

- `otel_trace_raw` receives a collection of span records from OpenTelemetry trace source performs stateful processing, extraction, and completion of trace-group-related fields.
- `otel_trace_group` fills in the missing trace group related fields in the collection of span records by looking up the OpenSearch backend.
- `service_map_stateful` performs the required preprocessing for trace data and builds metadata to displat the service map dashboard.

OpenSearch provides a generic sink that writes data to OpenSearch as the destination. The sink has configuration options related to the OpenSearch cluster, such as endpoint, SSL, username/passowrd, index name, index template and index stateu management.

### Log Analytics

Data Prepper supports receiving logs from OpenTelemetry Collector and processing those logs with a Grok Processor before ingesting them into OpenSearch through the OpenSearch sink.

# **letak gambar logs analytics kat sini**

In the application environment, the following components need to be prepared:

- OpenTelemetry Collector as intermediate component in transferring log data from instrumented device / application to DataPrepper.
- OpenSearch Dashboards as visualization and analysis tool.

The HTTP source will be used to receive data from OpenTelemetry Collector. This source accepts log data in a JSON array format. Grok Processor will be used for structuring and extracting important fields from the logs, allowing them to be query-able. The Grok Processor comes with wide variety of default patterns that match common log formats like Apache logs or syslogs, but it can easily accept any custom patterns to cater specific log format. OpenSearch will be used as the destination sink that comes with configuration options related to OpenSearch cluster such as endpoint, SSL, username / password, index temp,late and index state management.

### Metrics Analytics

Data-Prepper supports metrics ingestion into OpenSearch using the OpenTelemetry protocol. The OpenTelemetry Collector will act as agent of metrics acquisition, pulling serveral metrics endpoints or act as a receiver for others. Metrics are sent to Data-Prepper using the gRPC-based OpenTelemetry protocol. Data-Prepper receives the metrics, dissects and maps their data points, and saves each data point as an individual OpenSearch document.

# **letak gambar metrics analytics kat sini**

The OpenTelemetry metrics data model can be divided into 5 different types:

- Counter
- Gauge
- Histgogram
- Exponential Histogram
- Summary

Each metric type has a specific data point format. For example, counters and gauges use single value data points, while histograms and summaries used nested arrays to represent bucket of data.

The components for the metrics analytic will be identical as logs analytics.

## Objectives:
1. Deploy Data-Prepper to ingest data from OpenTelemetry Collector
2. Deploy OpenSearch as the application performance monitoring tool in the k8s cluster
3. OpenSearch Dashboard as the visualisation tool for the OpenSearch

## Sprint Plan:

### Subtasks:
- Data-Prepper k8s deployment manifest
- Data-Prepper configuration for trace pipelines
- Data-Prepper configuration for metrics pipeline
- Data-Prepper configuration for log pipeline
- Data-Prepper log pipeline parser using grok
- OpenSearch k8s deployment manifest
- OpenSearch k8s config map and service manifest
- OpenSearch Dashboard k8s deployment manifest
- OpenSearch Dashboard k8s configmap and service manifest
- OpenTelemetry collector config to export trace, metric and log data to Data-Prepper.