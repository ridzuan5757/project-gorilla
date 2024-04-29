# CloudBOS Instrumentation.

This document outlines the process and steps involved in instrumenting CloudBOS
application using Opentelemetry for distributed tracing, metrics, and logging.
OpenTelemetry will provide observability into the CloudBOS' performance and
behaviour, enabling better insights and troubleshooting capabilities.

## Objective
- Setting up local CloudBOS application sandbox with Zuhaili.
- Integrate OpenTelemetry into the Laravel backend for tracing requests and
  collecting metrics.
- Instrument Vue.js frontend to trace user interactions and frontend
  performance.
- Configure Opentelemetry exporters to send telemetry data to the Opentelemetry
  Gateway.

## Design Overview

### Architecture
- The backend API built with Laravel will be instrumented to trace incoming HTTP
  requests, database queries, and other relevant operations.
- The frontend application will be instrumented to trace user interactions,
  requests and frontend performance metrics.
- OpenTelemetry SDK will be used to instrument both the backend and frontend
  applications, capturing telemetry data.
- OpenTelemetry Collector will be configured to collect telemetry data to be
  send to Opentelemetry Gateway.

### Instrumentation Components
- Middleware will be added to intercept incoming HTTP requests and generate
  trace spans for each request lifecycle.
- Javascript plugin will be implemented to trace frontend interactions, such as
  request and route changes.
- OpenTelemetry SDK will be used to instrument custom code and capture
  additional metrics as needed.
- OpenTelemetry Collector exporters will be configured to send telemetry data to
  Opentelemetry Gateway.

### Implementation Plan

#### CloudBOS sandbox setup
- 1 day session with Zuhaili to setup local CloudBOS container application.
- Backend Instrumentation
- Frontend Instrumentation

