# Samsung PRISM – Week 2 Documentation

**Project:** Aegis Agent – AI-driven Consent Governance & Privacy Enforcement Platform

**Organization:** Samsung Research PRISM

**Module:** S6 – Biometric Consent & Policy Enforcement Framework

**Author:** Srikesh

**Reporting Period:** Week 2

**Focus:** Software Design & Architecture

---

## Document Overview

This document summarizes the software design and architectural work completed during Week 2 for the S6 – Biometric Consent & Policy Enforcement Framework. The work focuses on defining the overall system architecture, component organization, and runtime execution workflow that will serve as the foundation for subsequent implementation phases.

---

# Biometric Consent Architecture and Policy Enforcement Design

## 1. Module Scope & Design Objectives

### 1.1 Module Overview

The Biometric Consent & Policy Enforcement Framework (S6) enforces consent-aware access control for biometric data within the Aegis Agent platform. The module validates biometric consent at runtime, evaluates organizational policy rules, and enforces authorization decisions before biometric data is accessed or processed.

The framework is designed as a modular microservice that integrates with the enterprise authentication service, consent repository, object storage, and event-driven messaging services. It provides a centralized policy enforcement mechanism while maintaining compatibility with the overall PRISM architecture.

### 1.2 Design Scope

The S6 module focuses on three core components:

- **Biometric Consent Manager:** Manages biometric consent registration, retrieval, validation, updates, and expiry status.
- **Policy Decision Engine:** Evaluates access requests based on consent status, processing purpose, and organizational policies.
- **Access Enforcement Module:** Executes authorization decisions, blocks unauthorized operations, and generates audit events.

The module operates only on consent metadata and policy information. Biometric media files remain outside the module and are referenced through external object storage services.

### 1.3 Design Boundaries

**In Scope**

- Runtime biometric consent validation
- Policy-based authorization
- Consent status verification
- Access enforcement
- Audit event generation
- Integration with authentication, database, and messaging services

### 1.4 Design Objectives

The architecture is designed to:

- Provide centralized biometric consent enforcement.
- Perform real-time policy evaluation before data access.
- Support modular integration with adjacent work packages.
- Maintain scalability through a microservice-based architecture.
- Ensure secure communication using Keycloak, JWT, and OAuth 2.0.
- Generate auditable authorization decisions for compliance.

---

## 2. High-Level Architecture

![High-Level Architecture](images/high_level_architecture..jpg)

### 2.1 Architecture Workflow

The architecture follows a sequential request-processing pipeline consisting of authentication, consent validation, policy evaluation, and enforcement.

### 2.2 Step 1: User Authentication

The process begins when a user initiates a request to access a biometric-enabled enterprise application. The request is first forwarded to Keycloak, which authenticates the user using the configured identity provider.

Upon successful authentication, Keycloak generates a JWT containing the authenticated user's identity and authorization claims. The JWT is attached to subsequent requests and serves as the primary authentication credential for the S6 framework.

### 2.3 Step 2: REST API Layer

Authenticated requests enter the REST API Layer, implemented using FastAPI. This layer acts as the entry point for the S6 module. It validates incoming requests, extracts the JWT, performs request validation, and forwards requests to the internal business components.

The REST API Layer does not contain authorization logic. Its responsibility is to coordinate communication between external applications and internal services.

### 2.4 Step 3: Biometric Consent Manager

The request is processed by the Biometric Consent Manager, which is responsible for consent-related operations. It retrieves the user's consent metadata from PostgreSQL, verifies whether valid biometric consent exists, checks consent expiry, and confirms that the requested biometric type and processing purpose are covered by the recorded consent.

If consent information is invalid or unavailable, the request can be rejected before entering the policy evaluation stage.

### 2.5 Step 4: Policy Decision Engine

Once consent has been validated, the request is forwarded to the Policy Decision Engine. This component evaluates the request against predefined organizational policies stored in PostgreSQL.

The evaluation considers:

- Consent status
- Processing purpose
- Applicable policy rules
- Authorization constraints

Based on this evaluation, the engine generates an authorization decision such as **Allow**, **Deny**, **Mask**, **Delete**, or **Re-Consent Required**.

### 2.6 Step 5: Access Enforcement Module

The authorization decision is passed to the Access Enforcement Module, which acts as the enforcement point of the framework. This component applies the decision generated by the Policy Decision Engine and determines whether the requested biometric operation should proceed.

For approved requests, the module returns an authorization response to the enterprise application. For rejected requests, it blocks further processing and prevents unauthorized biometric access.

The module also publishes audit and enforcement events to Kafka/RabbitMQ, enabling asynchronous logging, monitoring, and downstream processing.

### 2.7 Step 6: Enterprise Application and Biometric Storage

After receiving a successful authorization response, the enterprise application retrieves the required biometric object from MinIO/AWS S3.

S6 does not store or directly access biometric media. It authorizes access to biometric resources while the actual biometric files remain securely stored in external object storage. This separation improves security and keeps authorization logic independent of storage infrastructure.

---

## 3. Component Architecture

![Component Architecture](images/component_architecture..jpg)

### 3.1 Component Responsibilities

The S6 module is organized into independent components with clearly defined responsibilities. Each component participates in the consent validation and access enforcement pipeline while maintaining separation of concerns.

| Component | Responsibility |
| --- | --- |
| REST API Layer | Receives REST requests, validates input, extracts authentication context, and routes requests to business services. |
| Biometric Consent Manager | Registers, updates, validates, retrieves, and checks expiry status for biometric consent metadata. |
| Policy Decision Engine | Evaluates consent status, validates processing purpose, reads policy rules, and generates authorization decisions. |
| Access Enforcement Module | Executes authorization decisions, generates authorization responses, and publishes audit and enforcement events. |
| PostgreSQL | Stores consent metadata and policy rules used by the consent and policy components. |
| Kafka/RabbitMQ | Receives audit and enforcement events for asynchronous processing and monitoring. |

### 3.2 REST API Layer

The REST API Layer provides the external interface for the S6 framework. It receives REST requests, validates request structure, verifies required metadata, and routes valid requests to the internal service layer.

Key responsibilities include:

- Receiving biometric access and consent management requests.
- Validating request payloads and required fields.
- Extracting authentication context from JWT access tokens.
- Routing requests to consent and policy services.

### 3.3 Biometric Consent Manager

The Biometric Consent Manager centralizes all consent metadata operations. It ensures that biometric access requests are evaluated against current and valid consent records.

Key responsibilities include:

- Registering biometric consent records.
- Updating existing consent metadata.
- Retrieving consent records for runtime checks.
- Validating consent status and expiry.
- Confirming that the requested processing purpose is covered by the recorded consent.

### 3.4 Policy Decision Engine

The Policy Decision Engine evaluates whether a biometric operation is permitted under the applicable consent state and policy rules.

Key responsibilities include:

- Evaluating consent status.
- Validating the requested processing purpose.
- Reading policy rules from PostgreSQL.
- Applying authorization constraints.
- Producing an authorization decision.

Supported decision outcomes include:

- **Allow**
- **Deny**
- **Mask**
- **Delete**
- **Re-Consent Required**

### 3.5 Access Enforcement Module

The Access Enforcement Module acts as the policy enforcement point. It applies the decision returned by the Policy Decision Engine and determines the response sent to the consuming enterprise application.

Key responsibilities include:

- Executing authorization decisions.
- Blocking unauthorized biometric operations.
- Returning authorization responses.
- Publishing audit events.
- Publishing enforcement events.

---

## 4. Runtime Workflow: Successful Execution Path

![Runtime Workflow](images/runtime_workflow_success..png)

### 4.1 Workflow Overview

The successful runtime workflow defines the execution path followed when a biometric access request is authenticated, consent is valid, applicable policy rules allow access, and the enterprise application is authorized to retrieve biometric media.

### 4.2 Execution Sequence

1. The user submits a biometric access request.
2. The REST API Layer receives the request.
3. The REST API Layer validates the JWT access token.
4. The request is forwarded to the Biometric Consent Manager.
5. The Biometric Consent Manager retrieves consent metadata from PostgreSQL.
6. The Biometric Consent Manager validates the consent record.
7. The request is forwarded to the Policy Decision Engine.
8. The Policy Decision Engine reads policy rules from PostgreSQL.
9. The Policy Decision Engine evaluates the authorization policy.
10. The Access Enforcement Module receives the policy decision.
11. The Access Enforcement Module generates the authorization response.
12. The module publishes an audit event to Kafka/RabbitMQ.
13. The enterprise application receives the authorization response.
14. The enterprise application retrieves authorized biometric media from MinIO/AWS S3.

### 4.3 Successful Path Result

In the successful execution path, biometric media access is permitted only after the request has passed authentication, consent validation, policy evaluation, and enforcement. The final media retrieval operation is performed by the enterprise application and remains outside the S6 service boundary.

---

# Week 2 Progress Summary

## Completed

- High-Level System Architecture
- Component Architecture
- Runtime Workflow (Successful Execution Path)

## Planned for Next Update

- Runtime Exception Handling Workflow
- Policy Decision Workflow
- Deployment Architecture
- Integration Design
- Design Decisions & Technical Rationale

---

**End of Week 2 Documentation**
