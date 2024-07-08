# Peer Forwarder

Peer Forwarder is an HTTP service that performs peer forwarding of a `event`
between `DataPrepper` nodes for aggregation. This HTTP service uses a hash-ring
approach to aggregate events and determine which `DataPrepper` node it should
handle on a given trace before routing it to that node. Currently, peer forwarder
is supported by the following processors:
- `aggregate`
- `service_map_stateful`
- `otel_trace_raw`

Peer Forwarder group events based on the identification keys provided by the
supported processors. For `service_map_stateful` and `otel_trace_raw`, the
identification keys are `traceId` by default and cannot be configured. The
`aggregate` processor is configured using the `identification_keys`
configuration option. From here, we can specify which keys to use for Peer
Forwarder.

Peer discovery allows `DataPrepper` to find other nodes that it will communicate
with. Currently, peer discovery is provided by:
- Static list
- DNS record lookup

## Discovery Modes - Static

Static discovery mode allows a `DataPrepper` node to discover nodes using a list
of IP addresses or domain names. This discovery modes can be implemented as
shown below:

```yaml
peer_forwarder:
  discovery_mode: static
  static_endpoints: ["data-prepper1", "data-prepper2"]
```

## Discovery Modes - DNS Lookup

DNS discovery is preferred over static discovery when scaling out `DataPrepper`
cluster. DNS discovery configures a DNS provider to return a list of 
`DataPrepper` hosts when given a single domain name. This list consists of a
***DNS A record*** and a list of IP addresses of a given domain.

```yaml
peer_forwarder:
  discovery_mode: dns
  domain_name: "data-prepper-cluster.my-domain.net"
```

# Tasks
- Peer forwarder configuration on DataPrepper cluster.
