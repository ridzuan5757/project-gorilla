# RBAC Authorization

Role-based access control (RBAC) is a method of regulating access to computer or
network resources based on the roles of individual users within the
organization. RBAC authorization uses the `rbac.authorization.k8s.io` API group
to drive authorization decisions, allowing users to dynamically configure
policies through the `k8s` API.

## API object

The RBAC API declares four kinds of `k8s` object:
- `Role`
- `ClusterRole`
- `RoleBinding`
- `ClusterRoleBinding`

## `Role` and `ClusterRole`

An RBAC `Role` or `ClusterRole` contains rules that represent a set of
permissions. Permissions are purely additive. A `Role` always sets permissions
within a particular `namespace` i.e when `Role`s are created, the `namespace`
where it belongs in has to be specified.

`ClusterRole`, by contrast, is a non-namespaced resource. The resources have
different names because a `k8s` object always has to be either namespaced or
not-namespaced; but it cannot be both.

`ClusterRoles` have several uses:
- Define permissions on namespaced resources and be granted access within
  individual `namespace`s.
- Define permissions on namespaced resources and be granted access across all
  `namespace`s.
- Define permissions on cluster-scoped resources.

In summary, if a role has to be defined within namespace, use a `Role`,
otherwise use `ClusterRole` for cluster-wide role.

## `RoleBinding` and `ClusterRoleBinding`

A role binding grants the permissions defined in a role to a user or set of
users. It holds a list of subjects, (users, groups, or service accounts), and a
reference to the role being granted. A `RoleBinding` grants permissions within a
specific `namespace` whereas a `ClusterRoleBinding` grants the access
cluster-wide.

A `RoleBinding` may reference any `Role` in the same `namespace`. Alternatively,
a `RoleBinding` can reference a `ClusterRole` and bind that `ClusterRole` to the
namespace of the `RoleBinding`. `ClusterRoleBinding` is used to bind
`ClusterRole` to all namespace of the cluster. The name of a `RoleBinding` or
`ClusterRoleBinding` object must be a valid path segment name.

# Tasks
- Implement ServiceAccount manifest for Opentelemetry DaemonSet agent
- Implement ServiceAccount manifest for Opentelemety Deployment gateway
- Implement ClusterRole manifest for Opentelemetry DaemonSet agent
- Implement ClusterRole manifest for Opentelemetry Deployment gateway
- Implement ClusterRoleBinding manifest for Opentelemetry DaemonSet agent
- Implement ClusterRoleBinding manifest for Opentelemetry Deployment gateway

