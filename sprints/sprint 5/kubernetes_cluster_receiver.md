# Kubernetes Cluster Receiver

|***Deployment Pattern***|***Usable***|
|---|---|
|`DaemonSet` agent|Will cause duplicate data.|
|`Deployment` gateway|Will cause duplicate data when there is more than 1 replica.|

The Kubernetes Cluster Receiver collects metrics and entity events about the
clsuter as a wholel using the `k8s` API server. This receiver will be used to
monitor:
- Pod phases
- Node conditions
- Other cluster-wide information

Since the receiver gathers telemetry for the cluster as a whole, ***only one
instance of the receiver is needed across the cluster in order to collect all
the data.***

There are different method of authentication, but typically `ServiceAccount` is
used. The `ServiceAccount` also needs proper permissions to pull data from the
`k8s` API server.

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: otel-collector-opentelemetry-collector
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: otel-collector-opentelemetry-collector
rules:
  - apiGroups:
      - ''
    resources:
      - events
      - namespaces
      - namespaces/status
      - nodes
      - nodes/spec
      - pods
      - pods/status
      - replicationcontrollers
      - replicationcontrollers/status
      - resourcequotas
      - services
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - apps
    resources:
      - daemonsets
      - deployments
      - replicasets
      - statefulsets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
    resources:
      - daemonsets
      - deployments
      - replicasets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - batch
    resources:
      - jobs
      - cronjobs
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - autoscaling
    resources:
      - horizontalpodautoscalers
    verbs:
      - get
      - list
      - watch
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: otel-collector-opentelemetry-collector
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: otel-collector-opentelemetry-collector
subjects:
  - kind: ServiceAccount
    name: otel-collector-opentelemetry-collector
    namespace: default
```

For node conditions, the receiver only collects `Ready` by default, but it can
be configured to collect more. The receiver can also be configured to report a
set of allocatable resources such as `cpu` and `memory`:

```yaml
k8s_cluster:
  auth_type: serviceAccount
  node_conditions_to_report:
    - Ready
    - MemoryPressure
  allocatable_types_to_report:
    - cpu
    - memory
```

# Tasks:
- Implement Kubernetes Cluster Receiver in OpenTelemetry Deployment Gateway.
- Configure `ClusterRole` for `k8s_cluster` receiver.
