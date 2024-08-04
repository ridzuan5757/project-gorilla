# Traefik as Nginx Ingress Replacement in K8S Cluster

This document outlines the plan and implementation on replacing exising `Nginx Ingress` controller with `Traefik` in current K8S cluster used for deploying Proactive Monitoring Project. This migration from `nginx-ingress` to `traefik` will provide enhanced routing, monitoring and scalability features, iproving overall cluster performance and manageability.

# Motivation
- Migrating from `Nginx Ingress` to `Traefik` without downtime.
- Leveraging `Traefik`'s features for routing, monitoring and scalability.
- Ensuring seamless integration for existing K8S infrastructure used for Proactive Monitoring deployment.

# Current Infrastructure Overview
- 3 Ingress resources managing traffic for the following services:
    - `OTLP` GRPC receiver of `opentelemetry-collector-daemonset-service` running in port `4317`.
    - `OTLP` HTTP receiver of `opentelemetry-collector-daemonset-service` running in port `4318`.
    - `opensearch-dashboard-service` running in port `5601`.

# Migration Reason
- Path-based routing feature on Nginx Ingress controller is not working when the K8S infrastructure is deployed in AWS.
- This would means `LoadBalancer`-type service need to be used for every services that need to be exposed to public.
- With this migration, a single ELB will be sufficient to expose all services that need public access via the `traefik` service. `traefik` will be responsible for routing requests to the appropriate services from its endpoints.

# Migration Plan

## Preparation
- Previous `nginx-ingress` configuration will be backed up. All current `nginx-ingress` resources will be exported.
- Current ingress resources will be reviewed for compatibility with `traefik`.

## Initial Configuration
- Create `K8S` manifest for ingress routes and middleware:
    - Define routes and backends for each services that need to be exposed to public.
    - Configure rate-limiting and custom headers for each services that need to be exposed to public using domain-based routing method.
    - Ensure service discovery is functioning correctly.

## Deployment
- Create `traefik` deployment and service.
- Configure RBAC permissions.
- Deploy all necessary resource objects related to `traefik`.

## Switch-over
- Update DNS records to point to `traefik` load balancer IP.
- Ensure smooth transition with minimal disruption.

## Validation
- Ensure `traefik` is routing traffic correctly:
    - `traefik` endpoint should be accessible to public via `LoadBalancer`-service and can verified with `kubectl get services` command.
    - All ingress resources can be accessed via AWS Route53 DNS, mapped to their respective services.

# Rollback Plan
`traefik` is expected to work in both bare-metal and AWS setup. In event where this condition is not met, a rollback plan back to `nginx-ingress` will be rolled out as follow:
- Apply the backed up `nginx-ingress` configuration.
- Point DNS records back to `nginx-ingress` load balancer IP.
- Ensure traffic is routed correctly through `nginx-ingress` service.

# Tasks
- Export all current `nginx-ingress` ingress resources to `traefik` ingress resources. [1]
- Create `traefik` deployment and service. [1]
- Configure RBAC permissions for `traefik`. [1]
- Setup `traefik` ingress routes and middlewares. [1]
- Reroute AWS Route53 DNS record of previous services routed by `nginx-ingress` to `traefik`. [1]
- Implement domain-based routing for the following services [3]:
    - `opentelemetry-collector-daemonset-service` on port `4317`
    - `opentelemetry-collector-daemonset-service` on port `4318`
    - `opensearch-dashboard` on port `5601`

