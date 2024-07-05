# Target Allocator

Target Allocator `TA` is an optional component of the OpenTelemetry Collector custom resource.

> [!NOTE]
> `TA` currently supports the `statefulset` and `daemonset` deployment modes of the OpenTelemetry Collector.

`TA` is a mechanism for decoupling service discovery and metrics collection functions of Prometheus such that they can be scaled independently. The collector manages Prometheus metrics without needing to install `prometheus`. The `TA` manages the configuration of the collector's prometheus receiver.

`TA` serves two functions:
- Even distribution of prometheus targets among a pool of Collectors.
- Discovery of Prometheus Custom Resources.

# Even Distribution of Prometheus Targets

`TA` first job is to discover targets to scrape and OpenTelemetry Collectors to allocate targets to. Then it can distribute the target it doscvers among the Collectors.

The Collectors in turn query the `TA` for metrics endpoint to scrape, and then the Colector's Prometheus Receivers srape the metrics target.

This means that the OTel Collectors collect the metrics instead of prometheus scraper.

sequenceDiagram
  participant Target Allocator
  participant Metrics Targets
  participant OTel Collectors
  Target Allocator ->>Metrics Targets: 1. Discover Metrics targets
  Target Allocator ->>OTel Collectors: 2. Discover available Collectors
  Target Allocator ->>Target Allocator: 3. Assign Metrics targets
  OTel Collectors ->>Target Allocator: 4. Query TA for Metrics endpoints scrape
  OTel Collectors ->>Metrics Targets: 5. Scrape Metrics target


## Allocation Strategy 

`per-node` strategy will be used by assigning each target to the collector running the same node the target is.

> [!WARNING]
> The `per-node` strategy ignores targets not assigned to a node, for example control-plane (master node) components.

