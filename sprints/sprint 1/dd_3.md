# Writing Vagrant and Ansible Scripts for k8s Cluster in Virtual Machines

This document outlines the process and steps involved in writing Vagrant and 
Ansible scripts to automate the deployment of a Kubernetes cluster. Vagrant will 
be used to provision virtual machines, while Ansible will configure the nodes 
and install Kubernetes components.

## Objectives
- Develop Vagrant scripts to define the infrastructure requirements for the 
  k8s cluster.
- Write Ansible playbooks to automate the installation and configuration of 
  k8s on the provisioned virtual machines.
- Test the deployment scripts to ensure they reliably create a functioning 
  k8s cluster.

## Sprint Plan

### Duration
Start Date:
End Date:

### Goals:
- **Vagrant Configuration**
    - Define the Vagrantfile to provision virtual machines for the k8s cluster.
    - Specify the desired virtual machines configurations, including memory, CPU
      and network settings.
- **Ansible Playbook Development**
    - Write Ansible playbooks to isntall necessary dependencies on each nodes.
    - Configure the master node with k8s components.
    - Configure the slave node(s) to join the k8s cluster.
    - Implement networking and DNS resolution for cluster communication.

## Backlog
- Define Vagrantfile with specifications for master and worker nodes.
- Write Ansible playbooks for installing k8s dependencies on all nodes.
- Develop Ansible tasks for configuring k8s components on the master node.
- Implement Ansible tasks for joining worker nodes to the k8s cluster.
- Configure networking and DNS resolution using Ansible roles.

