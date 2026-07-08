<div align="center">

# Consent Versioning & Policy Version Control + Consent Analytics & Governance Dashboard

### The version control state-engine and visualization command center of **PRISM CMP**

**Worklet 1 — Consent Collection, Mapping & Auto Metadata Generation**
Aegis Agent · AI-Driven Consent Governance & Privacy Enforcement Platform

<br>

![Worklet](https://img.shields.io/badge/Worklet-1-6E40C9?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Governance_&_Analytics-1F6FEB?style=for-the-badge)
![Compliance](https://img.shields.io/badge/Compliance-DPDP_2023_·_GDPR-2DA44E?style=for-the-badge)
![SLA](https://img.shields.io/badge/Dashboard_Latency-%3C2s-D29922?style=for-the-badge)

</div>

---

> [!IMPORTANT]
> **The thesis in one line.** Privacy policies and consent frameworks are living structures, not static text files. While other components capture consent or execute purges, **this module acts as the "brain" that tracks how privacy rules evolve over time and provides Data Protection Officers (DPOs) with the visual command center to monitor global compliance.**

---

## Table of Contents

| # | Section |
|---|---|
| 1 | [What This Topic Actually Is](#1-what-this-topic-actually-is-plain-decode) |
| 2 | [Where This Lives in the Project](#2-where-this-lives-in-the-project) |
| 3 | [The Policy Versioning State Machine](#3-the-policy-versioning-state-machine) |
| 4 | [The Governance Pipeline & Change Management](#4-the-governance-pipeline--change-management) |
| 5 | [The Two Hard Problems](#5-the-two-hard-problems-historical-reconstruction-vs-aggregation-latency) |
| 6 | [Consent Analytics Engine & Metric Derivation](#6-consent-analytics-engine--metric-derivation) |
| 7 | [Granular Auditing & Reporting Tiers](#7-granular-auditing--reporting-tiers) |
| 8 | [Data Model & a Robust Versioned Schema](#8-data-model--a-robust-versioned-schema) |
| 9 | [Open Problem & Research Direction](#9-open-problem--research-direction) |
| 10 | [Regulatory Mapping](#10-regulatory-mapping) |
| 11 | [Glossary](#11-glossary) |
| 12 | [Overall Workflow: Policy Update to Dashboard Refresh](#12-overall-workflow-policy-update-to-dashboard-refresh) |

---

## 1. What This Topic Actually Is (Plain Decode)

This topic represents the **systemic governance and visualization layer** of Worklet 1. It encompasses everything required to manage the lifecycle of a legal/privacy policy document and evaluate compliance health across all data repositories. It is split into three foundational pillars:

| Pillar | What it means | What triggers it |
|--------|---------------|------------------|
| **Policy Version Control** | Treating privacy notices like code. When a legal policy changes, it receives an immutable version identifier. The system tracks exactly which users agreed to which specific notice iteration, removing historical ambiguity. | Legal changes, new R&D purposes, or regulatory revisions. |
| **Consent Analytics Engine** | Processing metadata from millions of transactional consent actions to compute system health KPIs in real time (e.g., capture rates, active consent distributions, and compliance velocity). | Ingestion of raw consent tokens or real-time state changes from the network. |
| **Governance Dashboard** | The visual command center (DPO Web Console) providing continuous visibility into compliance indices, tracking SLA deadlines, and serving as a one-click export mechanism for regulatory audit packages. | DPO reviews, administrative checks, or preparation for regulatory audits. |

> [!NOTE]
> **The unifying idea:** If consent state and scope form the access-control truth for the data layer, **this component provides the versioned rulebook and the lens to inspect, verify, and report on that truth.**

---

## 2. Where This Lives in the Project

This component is the W1 deliverable named **"Governance Dashboard & Analytics."** It serves as the analytical layer of **Worklet 1**, reading transaction states from the core registries and summarizing operations for the presentation layer.

```mermaid
flowchart LR
    subgraph W1["WORKLET 1 — THIS COMPONENT (S7)"]
        DASH["Governance Dashboard<br/>React/Next.js · Tailwind"]
        ANALYTICS["Analytics Engine<br/>FastAPI · Aggregations"]
        DB[("PostgreSQL<br/>Policy Versions · Notice Matrix")]
    end

    subgraph W1_Core["WORKLET 1 — Core Capture"]
        CAPT["Consent Portal / API<br/>Capture UI (S3)"]
        LEDS[("Consent Ledger<br/>Append-Only Registry")]
    end

    W3["WORKLET 3<br/>Revocation & Lifecycle"]
    W14[("Blockchain Ledger<br/>Immutable Hashes (S14)")]
    SIEM["SIEM / Monitoring<br/>Prometheus · Grafana"]

    CAPT -->|emits transactional records| LEDS
    LEDS -->|streams state updates| ANALYTICS
    DB -->|provides active notice rules| CAPT
    W3 -->|broadcasts purge / lifecycle states| ANALYTICS
    W14 -->|verifies cryptographic blocks| DASH
    ANALYTICS -->|serves telemetry & data| DASH
    ANALYTICS -->|exposes logs| SIEM
