# Resources and Attributes Processor

This document outlines the design for the Resource and Attributes Processor that will be built in into OpenTelemetry Collector. This processor is responsible for modifying resource and attribute data within telemetry signals (`traces`, `metrics`, `logs`) based on defined rules mentioned in the subsequent sections. The primary goal is to provide a flexible mechanism to enrich, modify, and standardize telemetry data.

## Resources
`resources` are entities that produce telemetry data. They provide information about the environment where the telemetry data is collected. `resources` are typically associated with the entire telemetry pipeline and are used to describe the source of the data. This can include information about the service host, and any other relevant details about the environment. There are 2 processors that involves in enriching the telematry data that have to be build into OpenTelemetry Collector:
- Resource Detection Processor
- Resource Processor

## Attributes
`attributes` are key-value pairs that provides additional context to specific telemetry data points. They can be used to add contextual information to `trace`s, `metric`s and `log`s. Attributes are attached to individual `span`s, `metric`s or `log`s. They provide specific details about the operation being performed or the event being recorded. There is only one processors that will be used for this implementation, which is Attributes Processor.

## Key Differences

||***Resources***|***Attributes***|
|---|---|---|
|***Level of Application***|Applied to entire telemetry pipeline and describe the environment producing the telemetry data.|Applied to individual telemetry data points, such as specific spans, metrics, or logs, to provide additional context for those specific items.|
|***Usage***|Used to group and identify telemetry data from a particular source.|Used to add detailed context to each individual telemetry event, helping to understand the specifics of what happened at that moment.|

# Motivation
- Support various use cases for modifying resource and attributes data:
  - Telemetry data shall be labeled with host from where it is emitted.
  - Telemetry data shall be labeled with the source responsible for producing said data.
  - For example:
    - Metrics emitted by worker nodes shall be injected with `worker_node.id` label resource information.
    - Metrics that describes container information shall be injected with `container.name` resource information.
    - Metrics emitted from different environment stages shall me attributed appropriately.
  - Allow relevant personnels to define modification rules through `configmap` manifest file.
  - Ensure compatibility with existing OpenTelemetry Collector components.

# Resources Detection Processor

The Resource Detection Processor can be used to detect resource information from the host, based on the OpenTelemetry resource semantic conventions, and append or override the resource value in telemetry data with this information. As the processor is parsing information on the device level, it shall be only implemented on the `DaemonSet` agent deployment on infrastructure level.

## Detected Resources - System Metadata

This implementation will query the host machine to retrieve resource attributes regarding the host information as well as its operating system. By default, `host.name` is being set to FQDN if possible, and a hostname provided by operating system is used as fallback. The following specification shall be implemented: 

|***Resource Attributes***|***Enabled***|
|---|---|
|`host.arch`|`true`|
|`host.name`|`false`|
|`host.id`|`true`|
|`host.ip`|`true`|
|`host.mac`|`false`|
|`host.cpu.vendor.id`|`true`|
|`host.cpu.model.id`|`false`|
|`host.cpu.model.name`|`false`|
|`host.cpu.stepping`|`false`|
|`host.cpu.cache.l2.size`|`false`|
|`os.description`|`true`|
|`os.type`|`true`|

## Detected Resources - Docker Metadata

This implementation willquery the Docker daemon to retrieve the resource information that pertains to the container information. Docker socket `var/run/docker.sock` will be required to be mounted on the `DaemonSet` agent in order for this implementation to work. The following specification shall be implemented:

|***Resource Attributes***|***Enabled***|
|---|---|
|`host.name`|`true`|
|`os.type`|`true`|

## Detected Resources - AWS EC2 Metadata

This implementation use AWS SDK for Go to read resource information from the EC2 instance metadata API to retrieve EC2 related resource attributes. The following specification shall be implemented.

|***Resource Attributes***|***Enabled***|
|---|---|
|`cloud.provider`|`true`|
|`cloud.platform`|`true`|
|`cloud.account.id`|`true`|
|`cloud.region`|`true`|
|`cloud.availability_zone`|`true`|
|`host.id`|`true`|
|`host.image.id`|`true`|
|`host.name`|`true`|
|`host.type`|`true`|

# Resources Processor

The resource processor can be used to apply changes on resource attributes.
`attributes` represents actions that can be applied on resource attribute. The supported actions are as shown below:

|***Action***|***Description***|
|---|---|
|`insert`| Inserts a new attribute in input data where the ***key does not already exist***.|
|`update`| Update an attribute in input data where the ***key does exist***.|
|`upsert`| Perform insert or update. Inserts a new attribute in input data where the key does not already exist and updates an attribute in input data where the key does exist.|

For the actions `insert`, `update` and `upsert`:
- `key` is required.
- One of `value`, `from_attribute`, or `from_context` is required.
- `action` is required.


`insert` will be used for this implementation to prevent any implementation on the infrastructure level to overwrite any resource information that has been added on Hub level. This processor will be used to enrich the telemetry data with site information which will be mounted as volume. The following specification shall be implemented. 

|***Resource Attributes***|***Data Type***|***Action***|
|---|---|---|
|`site.name`|`string`|`insert`|
|`site.id`|`int32`|`insert`|
|`site.region`|`string`|`insert`|
|`site.postcode`|`int32`|`insert`|
|`site.city`|`string`|`insert`|
|`site.state`|`string`|`insert`|
|`site.latitude`|`float32`|`insert`|
|`site.longitude`|`float32`|`insert`|

# Attributes Processor

The attributes processor modifies attributes of span, log, or metric. This
processor also supports the ability to filter and match input data to determine
if they should be included or excluded for specific actions. It takes a list of actions which are performed in order as per specified in the config. This processor share the same configuration parameters as the Resources Processor.



This processor will be used to mark each telemetry data based on its development environment. The following specification shall be implemented.

|***Telemetry Attributes***|***Value***|
|---|---|
|`environment`|`development|staging|canary|production`|

# Configuration
The configuration for the Resource and Attributes Processor shall be defined via either:
- `configmap` manifest file for `DaemonSet` agent for `Deployment` gateway of the cluster.
- OpenTelemetry configuration `YAML` that will be mounted as volume on HUB level.


Tasks:
- Insert `k8s.node.name` for every `k8s`-related telemetry data generated by
  each `DaemonSet` node.
