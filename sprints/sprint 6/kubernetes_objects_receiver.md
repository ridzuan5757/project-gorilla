# Kubernetes Objects and Events Receiver

This document outlines the design for Kubernetes object and event receiver that will be built into OpenTelemetry Collector for the Proactive Monitoring infrastructure. These receivers designed to capture `K8S` objects and events and fed these information to the visualization component of the infrastructure.

# Motivation
- Provide mechanism for collecting `K8S` objects and events.
- Process and transform the collected data into a format suitable for the visualisation component of the Proactive Monitoring infrastructure.
- Ensure seamless integration with any FOSS visualisation tool.

# Specification

The Kubernetes Objects Receiver collects, either by pulling or watching, objects
from the `K8S` API server. The most common use case for this receiver is
watching `K8S` events, but it can be used to collect any type of `K8S` object.

The Kubernetes Events Receiver collects events from the `K8S` API server. It collects all the new or updated events that come in. These events serve as a detailed log, flagging changes, pod lifecycle events as well as any errors that occurs while the cluster is running. By monitoring these events, the relevant personnels able to stay informed about the stwate and activities within the cluster.

Since these receivers gathers telemetry for the cluster as a whole, ***only one
instance of the receiver is needed across the cluster in order to collect all
the data***.

This implementation consists of two main receivers withing the OpenTelemetry Collector:
- **Kubernetes Object Receiver** : Collectos metadata and status of Kubernetes objects such as Pods, Nodes and Services.
- **Kubernetes Event Receiver** : Captures `K8S` events that signify changes or updates within the cluster.

# Access Control

Since the processor uses the `k8s` API, it needs the correct permission to work
correctly. Since `serviceAccount` are the only authentication option available,
a proper `ClusterRole` must be configured. For any object that need to be
collected, we need to ensure the name is added to the `ClusterRole` manifest.

Currently only a `ServiceAccount` can be used for authentication. For objects
configured for *pulling*, the receiver will use the `k8s` API to periodically
list all the objects in the cluster. Each object will be converted to its own
log. For objects configured for *watching*, the receiver creates a stream with
the `k8s` API and which receives updates as the objects change.

| **Receiver**               | **Api Groups**  | **Resources**                   | **Verbs** |
|----------------------------|-----------------|---------------------------------|-----------|
| Kubernetes Object Receiver | `""`            | `events`                        | `get`     |
|                            |                 | `pods`                          | `list`    |
|                            |                 |                                 | `watch`   |
|                            | `events.k8s.io` | `events`                        | `list`    |
|                            |                 |                                 | `watch`   |
| Kubernetes Event Receiver  | `""`            | `events`                        | `get`     |
|                            |                 | `namespaces`                    | `list`    |
|                            |                 | `namespaces/status`             | `watch`   |
|                            |                 | `nodes`                         |           |
|                            |                 | `nodes/spec`                    |           |
|                            |                 | `pods`                          |           |
|                            |                 | `pods/status`                   |           |
|                            |                 | `replicationcontrollers`        |           |
|                            |                 | `replicationcontrollers/status` |           |
|                            |                 | `resourcequotas`                |           |
|                            |                 | `services`                      |           |
|                            | `apps`          | `daemonsets`                    | `get`     |
|                            |                 | `deployments`                   | `list`    |
|                            |                 | `replicasets`                   | `watch`   |
|                            |                 | `statefulsets`                  |           |
|                            | `extensions`    | `daemonsets`                    | `get`     |
|                            |                 | `deployments`                   | `list`    |
|                            |                 | `replicasets`                   | `watch`   |
|                            | `batch`         | `jobs`                          | `get`     |
|                            |                 | `cronjobs`                      | `list`    |
|                            |                 |                                 | `watch`   |
|                            | `autoscaling`   | `horizontalpodautoscalers`      | `get`     |
|                            |                 |                                 | `list`    |
|                            |                 |                                 | `watch`   |

# Expected Output

Output of the object receiver is predetermined by the cluster API resource. Every objects are listed via command `kubectl api-resources` shall be available for collection. The event data collected by the event receiver are as shown below:

| **Log**                 | **Event Name**         |
|-------------------------|------------------------|
| Event Reason            | `k8s.event.reason`     |
| Event Action            | `k8s.event.action`     |
| Event Start Time        | `k8s.event.start_time` |
| Event Name              | `k8s.event.name`       |
| Event Unique Identifier | `k8s.event.uid`        |
| Event Count             | `k8s.event.count`      |


# Tasks
- Implement Kubernetes Object Receiver and Kubernetes Event Receiver in the Deployment Gateway.
- Configure Service Account for Deployment Gateway
- Configure ClusterRole for Kubernetes Object receiver
- Configure ClusterRoleBinding for the ServiceAccount and ClusterRole
