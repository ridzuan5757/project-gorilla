# Kubernetes Attributes Processor

|***Deployment Pattern***|***Usable***|
|---|---|
|DaemonSet agent|Yes|
|Deployment gateway|Yes|
|Sidecar|No|

The Kubernetes Attributes Processor automatically discovers kubernetes pods,
extract their metadata, and adds the extracted metadata to spans, metrics, and
logs as resource attributes.

Because it adds kubernetes context to the telemetry, this processor lets us
correlate the application's traces, metrics, and logs signals with the
kubernetes telemetry, such as pod metrics and traces.

This processor uses the kubernetes API to discover all pods running in a cluster
and keeps a record of their IP addresses, pod UIDs, and interesting metadata. By
defauly, data passing through the processor is associated to a pod via the
incoming request's IP address, but different rules can be configured. Since the
processor uses the kubernetes API, a role permission would be required.

The following attributes are added by default:
- `k8s.namespace.name`
- `k8s.pod.name`
- `k8s.pod.uid`
- `k8s.pod.start_time`
- `k8s.deployment.name`
- `k8s.node.name`

This processor can also set custom resource attributes for traces, metrics and
logs using the kubernetes labels and kuberentes annotations we have added to the
pods and namespaces.

```yaml

```
