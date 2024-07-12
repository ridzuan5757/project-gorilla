# Kubeletstats Receiver

|***Deployment Pattern***|***Usable***|
|---|---|
|`DaemonSet` agent|yes|
|`Deployment` gateway|Yes, but will only collect metrics from the node it is deployed on|

Each `k8s` node runs a kubelet that includes an API server. This receiver
connects to that kubelet via the API server to collect metrics about the node
and the workloads running on the node.

There are method of authentication to the API server will be based on
`ServiceAccount`. This `ServiceAccount` will require proper permissions to pull
data from the Kubelet.

By default, metrics will be collected for pods and nodes, but the receiver can
be configured to collect container and volume metrics as well. The receiver also
allows configuring how often the metrics are collected:

```yaml
receivers:
    kubeletstats:
        collection_interval: 10s
        auth_type: serviceAccount
        endpoint: ${env:K8S_NODE_NAME}:12050
        insecure_skip_verify: true
        metric_groups:
            - node
            - pod
            - container
```

## Extra metadata labels

By default, all produced metrics get resource labels based on what kubelet
stats or summary endpoint provides. For some use cases it might not be enough.
So it is possible to leverage other endpoints to fetch additional metadata
entities and set them as extra labels on metric resource. Currently supported
metadata include the following:
- `container.id` to augment metrics with Container ID label obtained from
  container statuses exposed via `/pods`.
- `k8s.volume.type` to collect volume type from the Pod spec exposed via `/pods`
  and have it as a label on volume metrics. If there is more information
  available from the endpoint than just volume type, those are synced as well
  depending on the available fields and the type of the volume. For example,
  `aws.volume.id` would be synced from `awsElasticBlockStore` and `gcp.pd.name`
  is synced for `gcePersistentDisk`.

`extra_metadata_labels` field need to be added alongside with `container.id` and
`k8s.volume.label` in order to add these labels to the metrics:

```yaml
eceivers:
  kubeletstats:
    collection_interval: 10s
    auth_type: "serviceAccount"
    endpoint: "${env:K8S_NODE_NAME}:10250"
    insecure_skip_verify: true
    extra_metadata_labels:
      - container.id
```

## Metric Groups

A list of metric groups from which metrics should be collected. By default,
metrics from containers, pods and nodes will be collected. If `metric_groups` is
set, only metrics from the listed groups will be collected.

Valid groups are:
- `container`
- `pod`
- `node`
- `volume`

For example, if we are looking to collect only `node` and `pod` metrics from the
receiver, the configuration would be as follow:

```yaml
receivers:
  kubeletstats:
    collection_interval: 10s
    auth_type: "serviceAccount"
    endpoint: "${env:K8S_NODE_NAME}:10250"
    insecure_skip_verify: true
    metric_groups:
      - node
      - pod
```

## CPU node utilization as ratio of total node's capacity.

In order to calculate the node utilization metrics, the information of the
node's capacity must be retrieved from the `k8s` API. In this, the
`k8s_api_config` needs to be set. In addition, the node name must be identified
property. The `K8S_NODE_NAME` env var can be set using the dowward API inside
the collector pod `spec` as follows:

```yaml
env:
  - name: K8S_NODE_NAME
    valueFrom:
      fieldRef:
        fieldPath: spec.nodeName
```

Then set the `node` value to `${env:K8S_NODE_NAME}` in the receiver's
configuration:

```yaml
receivers:
    kubeletstats:
      collection_interval: 10s
      auth_type: 'serviceAccount'
      endpoint: '${env:K8S_NODE_NAME}:10250'
      node: '${env:K8S_NODE_NAME}'
      k8s_api_config:
        auth_type: serviceAccount
      metrics:
        k8s.container.cpu.node.utilization:
          enabled: true
        k8s.pod.cpu.node.utilization:
          enabled: true
```

## Role-based access control

This receiver needs to `get` permissions on the `nodes/stats` resources.
Additionally, when using `extra_metadata_labels` or any of the 
`{request | limit}_utilization` metrics the processor also needs `get`
permissions for `nodes/proxy` resources.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: otel-collector
rules:
  - apiGroups: [""]
    resources:
      - "nodes/stats"
    verbs: ["get"]
    
  # Only needed if you are using extra_metadata_labels or
  # are collecting the request/limit utilization metrics
  - apiGroups: [""]
    resources: ["nodes/proxy"]
    verbs: ["get"]
```

Task:
- `ServiceAccount` for Kubeletstats Receiver.
- `ClusterRole` for KubeletStats Receiver.
- `ClusterRoleBinding` for KubeletStats Receiver.
- `K8S_NODE_NAME` environment variable for CPU node utilization metrics.
