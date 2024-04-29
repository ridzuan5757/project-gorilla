# Setting up On-Premise Kubernetes Cluster with 1 Master Node and 1 Worker Node

This document outlines the process and steps involved in setting up an
on-premise k8s cluster with:
- 1 master node
- 1 slave node.

The cluster will serve as a foundation for deploying and managing containerized
applications in a local environment.

## Objectives
- Provision hardware for the k8s cluster nodes.
- Install and configugure k8s components on the master and worker nodes.
- Establish communication and networking between the master and worker nodes.
- Verify the cluster setup and basic functionality.
- Distribute the config file to the relevant personnels.

## Sprint Plan

### Duration
Start Date: 08-05-23
End Date: 10-05-23

### Goals
- **Infrastructure Provisioning and k8s Installation**
    - Set up hardware for the master and the slave node.
    - Disable swap memory for the system.
    - Ensuring that the Docker is running using Containerd engine.
    - Ensuring that Containerd is running under `systemd` control group.
- **Cluster Configuration and Networking**
    - Confogure the k8s master node with necessary settings and configuration.
    - Join the slave node to the k8s cluster.
    - Establish networking between the master and slave node.
- **Cluster Verification and Testing**
    - Verify the cluster setup by deploying a sample application or workload.
    - Test basic cluster functionalities such as pod scheduling, service
      discovery and networking.

## Backlog
- Procure and allocate hardware resources for hosting the k8s nodes.
- Install suitable operating system on the master and worker nodes.
- Install container runtime on both nodes.
- Configure k8s on master node, including API server, controller manager,
  scheduler and etcd.
- Join the slave node to the k8s cluster using join token.
- Configure networking to enable communication between master and worker nodes.
- Deploy sample application or workload to test cluster functionality.


