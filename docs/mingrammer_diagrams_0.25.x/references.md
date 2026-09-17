# Mingrammer Diagrams (0.25.x) Documentation Reference

Crawled from [https://diagrams.mingrammer.com](https://diagrams.mingrammer.com/docs/getting-started/installation) — the official documentation for the **diagrams** Python library, which lets you prototype cloud system architecture diagrams as pure Python code (powered by Graphviz).

## Getting Started

- **001 - [Installation](references/001_installation.md)** — Prerequisites and setup: `diagrams` requires Python 3.7+ and a Graphviz installation (via Homebrew, Chocolatey, or Winget). Shows install commands for pip, pipenv, poetry, and uv, plus a Quick Start example (`ELB >> EC2 >> RDS`) and the `diagrams` CLI for processing multiple diagram files at once.

- **002 - [Examples](references/002_examples.md)** — Nine complete, copy-pasteable architecture examples: Grouped Workers, Clustered Web Services, Event Processing on AWS, Message Collecting on GCP, Exposed Pod with 3 Replicas and Stateful Architecture on Kubernetes, Advanced Web Service with On-Premises (plain, and with colors/labels), and RabbitMQ Consumers with custom nodes. A good starting point for realistic diagram code.

## Guides

- **003 - [Diagrams](references/003_diagrams.md)** — The `Diagram` object, the primary context of every diagram. Covers the basic `with Diagram(...)` pattern, rendering inside Jupyter notebooks, output format options (`outformat` for png/jpg/svg/pdf/dot, including multi-format lists), custom `filename`, disabling auto-open with `show=False`, and custom Graphviz attributes (`graph_attr`, `node_attr`, `edge_attr`).

- **004 - [Nodes](references/004_nodes.md)** — The `Node` object representing a system component, consisting of provider, resource type, and name (e.g., `EC2` = aws + compute). Shows how to import nodes from all providers and explains data flow operators `>>`, `<<`, `-`, the `direction` parameter (TB/BT/LR/RL), operator-precedence caveats, and grouping nodes into lists for bulk connections.

- **005 - [Clusters](references/005_clusters.md)** — The `Cluster` object for grouping nodes into isolated, visually framed regions, with examples of connecting nodes inside and outside clusters and arbitrarily deep nested clusters (no depth limit) for complex architectures.

- **006 - [Edges](references/006_edges.md)** — The `Edge` object for styling connections between nodes with `label`, `color`, and `style` attributes that mirror Graphviz edge attributes. Includes a large colored on-premises example plus two techniques to reduce edge noise: blank placeholder nodes ("Less Edges") and merged edges via the `concentrate` Graphviz attribute.

## Nodes

- **007 - [OnPrem](references/007_onprem.md)** — Full catalog of on-premises node classes (400+ lines): aggregators, analytics (Spark, Hive, Databricks), CI/CD, containers, databases (PostgreSQL, MySQL, Redis), gitops, in-memory stores, logging, monitoring (Grafana, Prometheus), networking, queues (Kafka), storage, and more, organized by sub-module.

- **008 - [AWS](references/008_aws.md)** — Largest provider catalog (1000+ lines): all AWS node classes across analytics, compute (EC2, Lambda, ECS, EKS), cost, database (RDS, Redshift, DynamoDB), developer tools, IoT, management, media, migration, ML, mobile, networking (VPC, ELB, Route53), robotics, security, and storage (S3), grouped by service category with aliases.

- **009 - [Azure](references/009_azure.md)** — The biggest page (1600+ lines): complete Azure node classes from AI/Machine Learning (AzureOpenai, CognitiveServices, BotServices), analytics, compute, containers, database, devops, identity, integration, IoT, management/governance, migration, monitoring, networking, security, storage, and web.

- **010 - [GCP](references/010_gcp.md)** — Google Cloud node classes: analytics (BigQuery, Dataflow, Pub/Sub), API (APIGateway, Apigee), compute (AppEngine, GKE), database, developer tools, IoT, management, and migration categories.

- **011 - [IBM](references/011_ibm.md)** — IBM Cloud node classes: analytics, applications, blockchain, compute, data, devops, general, infrastructure, management, network, security, social, storage, and user categories.

- **012 - [K8S](references/012_k8s.md)** — Kubernetes node classes: chaos, cluster config, compute (Pod, Deploy/Deployment, STS/StatefulSet), control plane (API/APIServer, CM/ControllerManager), network, orchestration, RBAC, scheduling, storage, and system, with common aliases.

- **013 - [AlibabaCloud](references/013_alibabacloud.md)** — Alibaba Cloud node classes: analytics, application, compute (ECS), database, integration, network, security, and storage categories.

- **014 - [OCI](references/014_oci.md)** — Oracle Cloud Infrastructure node classes: compute, database, developer services, governance, identity, integration, monitoring, network, security, and storage, with `White` variants.

- **015 - [OpenStack](references/015_openstack.md)** — OpenStack node classes: API proxies, application lifecycle, bare metal, compute, database, identity, networking, security, storage, and workload provisioning.

- **016 - [Firebase](references/016_firebase.md)** — Firebase node classes: base, develop (Authentication, Firestore, Functions, Hosting, ML Kit, Realtime Database), and growth (Analytics, Crashlytics, Predictions, Remote Config).

- **017 - [DigitalOcean](references/017_digitalocean.md)** — DigitalOcean node classes: compute (Droplet, Containers, K8SCluster), database, network (LoadBalancer, VPC), and storage.

- **018 - [Elastic](references/018_elastic.md)** — Elastic Stack node classes: agent, beats (Filebeat, Metricbeat, APM), Elasticsearch, enterprise search, observability, orchestration, SaaS, and security.

- **019 - [Outscale](references/019_outscale.md)** — Outscale node classes: compute, network (ClientVpn, InternetService, LoadBalancer, NatService, Net), and storage.

- **020 - [Generic](references/020_generic.md)** — Generic/vendor-neutral node classes: blank, compute, database, device, network, OS, place, storage, and virtualization (for abstract or conceptual diagrams).

- **021 - [Programming](references/021_programming.md)** — Programming-related node classes: flowchart shapes (Action, Decision, Database, Document, InputOutput, LoopLimit, etc.), framework, language, and workflow categories.

- **022 - [Saas](references/022_saas.md)** — SaaS node classes: alerting (Pagerduty, Opsgenie, Newrelic), analytics (Snowflake), automation (n8n), cdn, collaboration, communication, crm, identity, marketing, media, social, and support.

- **023 - [C4](references/023_c4.md)** — How to create C4 model diagrams (c4model.com) using the `diagrams.c4` package: `Person`, `Container`, `Database`, `System`, `SystemBoundary`, and `Relationship` classes, with a full Internet Banking System container diagram example.

- **024 - [Custom](references/024_custom.md)** — Using the `Custom` node class with your own icons, both from local image files (a Creative Commons attribution example) and from remote URLs, to add bespoke components not covered by built-in providers.

- **025 - [GIS](references/025_gis.md)** — Geographic Information System node classes: CLI tools (Gdal, Mapnik, Pdal), data sources (Openstreetmap, Here, IGN), database, desktop, formats, geocoding, JavaScript/Python libraries, OGC standards, routing, and servers.

---

> **Note:** Index compiled from the actual page content of `docs/mingrammer_diagrams_0.25.x/references/` after crawling. Each entry links to its full Markdown file.
