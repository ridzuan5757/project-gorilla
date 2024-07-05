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
k8sattributes:
  auth_type: 'serviceAccount'
  extract:
    metadata: # extracted from the pod
      - k8s.namespace.name
      - k8s.pod.name
      - k8s.pod.start_time
      - k8s.pod.uid
      - k8s.deployment.name
      - k8s.node.name
    annotations:
      # Extracts the value of a pod annotation with key `annotation-one` and inserts it as a resource attribute with key `a1`
      - tag_name: a1
        key: annotation-one
        from: pod
      # Extracts the value of a namespaces annotation with key `annotation-two` with regexp and inserts it as a resource  with key `a2`
      - tag_name: a2
        key: annotation-two
        regex: field=(?P<value>.+)
        from: namespace
    labels:
      # Extracts the value of a namespaces label with key `label1` and inserts it as a resource attribute with key `l1`
      - tag_name: l1
        key: label1
        from: namespace
      # Extracts the value of a pod label with key `label2` with regexp and inserts it as a resource attribute with key `l2`
      - tag_name: l2
        key: label2
        regex: field=(?P<value>.+)
        from: pod
  pod_association: # How to associate the data to a pod (order matters)
    - sources: # First try to use the value of the resource attribute k8s.pod.ip
        - from: resource_attribute
          name: k8s.pod.ip
    - sources: # Then try to use the value of the resource attribute k8s.pod.uid
        - from: resource_attribute
          name: k8s.pod.uid
    - sources: # If neither of those work, use the request's connection to get the pod IP.
        - from: connection
```

There are also special configuration options for when the collector is deployed
as kubernetes daemonset or as deployment gateway.

## Deployment Scenarios

The processor can be used in collectos deployed both as:
- `DaemonSet` agent
- `Deployment` gateway

### As an agent

When running as an agent, the processor detects IP addresses of pods sending
spans, metrics or logs to the agent and uses this information to extract
metadata from pods.

When running as an agent, it is important to apply a discovery filter so that
the processor only discover pods from the same host that it is running on. Not
using such a filter can result in unnecessary resource usage especially on very
large clusters. Once the filter is applied, each processor will only query the
`k8s` API for pods running on it's own node.

Node filter can be applied by setting the `filter.node` config option to the
name of a `k8s` node. While this works as expected, it cannot be used to
automatically filter pods by the same node that the processor is running on in
most cases as it is not know beforehand which node a pod will be scheduled on.

However, `k8s` has a solution for this called ***downward API***. To
automatically filter pods by the node the processor is running on, the following
requirements need to be cleared:

Use the downward API to inject the node name as an environment variable. Add the
following snippet under the pod env section of the Opentelemetry container. This
will inject a new environment variable to the Opentelemetry container with the
value as the name of the node the pod was scheduled to run on.

```yaml
spec:
  containers:
  - env:
    - name: KUBE_NODE_NAME
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: spec.nodeName
```

Set the `filter.node_from_env_var` value to the name of the environment variable
holding the node name. This will restrict each OpenTelemetry agent to query pods
running on the same node only, reducing resource requirements for very large
clusters.

```yaml
k8sattributes:
    filter:
        node_from_env_var: kUBE_NODE_NAME
```

### As a gateway

When running as a gateway, the processor cannot correctly detect the IP address
of the pods generating the telemetry data without any of the well-known IP
attributes, when it receives them from an agent instead of receiving them
directly from the pods. To workaround this issue, agents deployed with this
processor can be configured to detect the IP addresses and forward them along
with the telemetry data resources.

Collector can then match this IP address with the `k8s` pods and enrich the
records with the metadata. In order to set this up, the following requirements
need to be cleared:

Setup agents in passthrough mode by configuring the agents' processor value to
true. This will ensure that the agents detect the IP address as add it as an
attribute to all telemetry resources. Agents will not make any `k8s` API calls,
do nay discovery pods or extract any metadata.

```yaml
k8sattributes:
    passthrough: true
```

Configure the collector as usual. No special configuration changes ar eneeded to
be made on the collector. It will automatically detect the IP address of spans,
logs and metrics sent by the agents as well as directly by other services or
pods.

Tasks:
- Opentelemetry DaemonSet node name environment export.
- Opentelemetry k8s attribute processor node filter.
- Opentelemetry k8s attribute processer passthrough configuration.

