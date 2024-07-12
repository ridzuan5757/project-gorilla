# `traefik`

`traefik` is an open-source edge router that enable `Services` to be published.
It receives requests on behlf of the system and finds out which components are
responsible for handling them.

`traefik` is based on the concept of `EntryPoints`, `Routers`, `Middlewares`,
and `Services`. The main features include dynamic configuration, automatic
service discovery, and support for multiple backends and protocols.

- `EntryPoints` are the network entry points into `traefik`. They define the
  port which will receive the packets, and whether to listen for TCP or UDP.
- `Routers` is on charge of connecting incoming requests to the services that can handle them.
- `Middlewares` is an extension to  `Routers` to modify requests or responses before they are sent to your services.
- `Services` are responsible for configuring how to reach the actual services that will eventually handle the incoming services that will eventually handle the incoming requests.

## Edge Router

`traefik` is an edge router, this means that it is the door to your platform, and that will intercepts and routes every incoming request - it knows all the logic and every rule that determine which services handle which requests based on:

- path
  - header
  - host

## Auto Service Discovery

Where traditionally edge routers or reverse proxies need a configuration file that contains every possible route to the services, `traefik` gets them from the services themselves.

In order to deploy the `Service`s, we attach information that tells `traefik` the characteristics of the requests the `service`s can handle.

This means that when a `Service` is deployed, `traefik` detects it immediately and updates the routing rules in real time. Similarly, when a `Service` is removed from the infrastructure, the correspoding route is deleted accordingly.

## `traefik` use case with `k8s`

`traefik` use `k8s` API to discover running `Services`. To use the `k8s` API, `traefik` needs some permissions. This permission mechanism is based on roles defined by the cluster administrator. The role is then bound to an account used by an application , in this case `traefik` proxy.

The first step is to create the role. `ClusterRole` resource enumerates the resources and actions available for the role.

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: traefik-role

rules:
  - apiGroups:
      - ""
    resources:
      - services
      - endpoints
      - secrets
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
      - networking.k8s.io
    resources:
      - ingresses
      - ingressclasses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - extensions
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - update
```

The next step is to create a dedicated service account for `traefik`.

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: traefik-account
```

And then, bind the role on the account to apply the permissions and rules on the latter.

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: traefik-role-binding

roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: traefik-role
subjects:
  - kind: ServiceAccount
    name: traefik-account
    namespace: default
```

## Deployment

The ingress controller is a software that runs in the same way as any other application on a cluster. To start `traefik` on the `k8s` cluster, a `Deployment` resource must exist to describe how to configure and scale contaners horizontally to support larger workloads.

```yaml
kind: Deployment
apiVersion: apps/v1
metadata:
  name: traefik-deployment
  labels:
    app: traefik

spec:
  replicas: 1
  selector:
    matchLabels:
      app: traefik
  template:
    metadata:
      labels:
        app: traefik
    spec:
      serviceAccountName: traefik-account
      containers:
        - name: traefik
          image: traefik:v3.0
          args:
            - --api.insecure
            - --providers.kubernetesingress
          ports:
            - name: web
              containerPort: 80
            - name: dashboard
              containerPort: 8080
```

The `Deployment` contains an important attribute for customizing `traefik` - `args`. These arguments are the static configuration for `traefik`. From here, it is possible to enable the dashboard, configure entry ponts, select dynamic configuration providers and more.

In ths `deployment`, the static configuration enables the `traefik` dashboard, and uses `k8s` native ingress resources as router definitions to route incoming requests.

A deployment manages scaling and then create lots of containers, called `pods`. Each `pod` is configured following `spec` field in the `deployment`.

Given that, a `deployment` can run multiple `traefik` proxy `pod`s, a piece is required to forward the traffic to any of the instance: namely `Service`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: traefik-dashboard-service

spec:
  type: LoadBalancer
  ports:
    - port: 8080
      targetPort: dashboard
  selector:
    app: traefik
---
apiVersion: v1
kind: Service
metadata:
  name: traefik-web-service

spec:
  type: LoadBalancer
  ports:
    - targetPort: web
      port: 80
  selector:
    app: traefik
```