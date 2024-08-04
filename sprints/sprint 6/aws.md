# AWS Account Setup for Proactive Monitoring Initiative

The Proactive Monitoring Initiative Project aims to enhance the monitoring, logging, and tracing capabilities of our infrastructure and applications. This will enable proactive identification and resolution of issues, ensuring high availability and performance of the organization ecosystem such as Hub, CloudBOS, POS, and PDT. The project will utilize AWS services to achieve comprehensive observability, including real-time monitoring, centralized logging, and distributed tracing, ensuring optimal performance, reliability, and security of our applications and infrastructure.

# Motivation
- Creating new AWS account exclusively for Proactive Monitoring Initiative Project - related deployments.
- Migrating current Proactive Monitoring infrastructure from staging account to new account.

# Account Structure
- ***New Account Justification*** : A new AWS account will be created to isolate observability resources from other environments, ensuring dedicated management and billing.
- ***Account Naming*** : The new account will be named `proactive-monitoring`.

# Account Naming and Tagging
- ***Resource Naming Convention*** : A consistent naming convention will be enforced: <service>-<environment>-<purpose>, e.g., ec2-prod-monitoring.
- ***Tagging Policy*** : The following tags convention to all resources will be enforced:
    - `silentmode:owner`: `engineering`
    - `silentmode:environment`: `development | staging | canary | production`
    - `silentmode:service`: `proactive-monitoring`

# Security and Compliance

## IAM Roles and Policies
- ***Administrator Role*** : Full access to manage all AWS services.
- ***Support Role*** : Limited read and write monitoring and logging data.
- ***Policy Example*** : Developers will have a policy granting permissions to CloudWatch, S3, and SQS.


## Data Encryption:
- ***At Rest*** : AWS KMS will be used to encrypt data stored in S3 and EBS volumes.
- ***In Transit*** : Enforce SSL/TLS for all data transmission.

# Observability Tools and Services
Not applicable. Purpose of the proactive monitoring initiative is to eliminate the need on any third party observability services.

# Cost Management - Budgeting and Forecasting
- ***AWS Budget*** : Set up and AWS Budget to monitor spending, with alerts for thresholds.
- ***Cost Allocation Tags*** : See # Account Naming and Tagging section.

# Backup and Disaster Recovery Strategies
- Telemetry data type such as `metrics`, `traces`, and `logs` are considered to be non-critical and would not be backed up.
- 21-days retention policy will be applied to all telemetry data stored in S3, ensuring regular audits and compliance.

# Deployment and Automation
- ***Tools*** :
    - AWS CloudFormation generator such as AWS CDK or Hashicorp Teraform will be used as resource provisioning and management.
    - Cloud formation templates or source codes for AWS CDK will be stored in the organization Gitlab repository for versioning and collaborative development.

# Credential Management - AWS Access Keys
- ***Policy*** :
    - Access keys usage will only be used exclusively for deployment and automation.
    - IAM roles with temporary credentials will be used for other purposes.
- ***Rotation*** :
    - Policy to rotate access keys every 90 days will be implemented.

# Documentation and Knowledge Sharing
- *** Platform *** :
    - Confluence will be used exclusively for project documentation that pertains to non-developers.
    - Gitlab README markdown files will be used for project documentation that pertains to developers only.
- *** Content *** : Document setup instructions, configurations, and troubleshooting guides.

# Approval and Implementation Process
- ***Workflow*** : Submit a request for account creation to the Principal Software Engineer for approval.
- ***Stakeholder Review*** : Ensure interested stakeholders review and approve the proposed setup.

# Deployment Plan
- Rolling update with rollback strategy will be enforced on any update on the Kubernetes infrastructure.
- Deployment process will be monitored and any issues will be immediately addressed.

# Post-Deployment Support
- Support roles for ongoing maintenance and incident response will be defined.
- Procedures for scaling kubernetes resource and adapting to new requirements are as shown below:
    - Horizontal pod autoscaling will be used to address the need to add extra replica to the other worker nodes any pressure on either CPU, disks or memory.
    - Extra worker nodes with same specification will be added as needed if the aforementioned steps fail to address this issue. Pod reallocation to the new worker nodes will be handled automatically by the control-plane nodes.

# Review and Continuous Improvement
- Reviews of AWS account setup and any resource that pertains to this project will be scheduled on quarterly basis.
- Improvement based on feedbacks, root-cause analysis and lesson learned will be implemented as needed.

# Tasks
- Create new AWS account for Proactive Monitoring Initiative Project. [1]
- Create accounts with admin access for the relevant personnels. [1]
- Setup AWS Budget to monitor spending, with alerts for thresholds. [1]
- Migration of Proactive Monitoring infrastructure from staging account to proactive-monitoring account [2]