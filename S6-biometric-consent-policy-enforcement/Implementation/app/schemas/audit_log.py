"""Pydantic schemas for immutable audit log records."""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.common import SchemaBase
from app.schemas.enums import AuditAction, AuditDecision


class AuditLogCreate(SchemaBase):
    """Schema for creating an authorization audit record."""

    user_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="External identity of the user tied to the audit event.",
        examples=["user_12345"],
    )
    consent_id: UUID = Field(
        ...,
        description="Consent record referenced by the audit event.",
        examples=["7b9f0b9f-d3a1-4c2c-b7a1-0b0a4f7f9c10"],
    )
    policy_id: UUID = Field(
        ...,
        description="Policy record referenced by the audit event.",
        examples=["a9a36b83-fc50-451c-92c3-2e1f2d9a126f"],
    )
    request_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Correlation identifier for the audited request.",
        examples=["req_01J2Z7F3Q8EXAMPLE"],
    )
    action: AuditAction = Field(
        ...,
        description="Authorization workflow action that was audited.",
        examples=[AuditAction.CONSENT_CHECK],
    )
    decision: AuditDecision = Field(
        ...,
        description="Decision captured for the audited action.",
        examples=[AuditDecision.ALLOW],
    )
    message: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional human-readable audit message.",
        examples=["Consent is active and valid for the requested purpose."],
    )


class AuditLogResponse(SchemaBase):
    """Schema returned for immutable authorization audit records."""

    audit_id: UUID = Field(
        ...,
        description="Unique audit log identifier.",
        examples=["bdce9c1f-8028-4a4c-a45b-09daec5d2c27"],
    )
    user_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="External identity of the user tied to the audit event.",
        examples=["user_12345"],
    )
    consent_id: UUID = Field(
        ...,
        description="Consent record referenced by the audit event.",
        examples=["7b9f0b9f-d3a1-4c2c-b7a1-0b0a4f7f9c10"],
    )
    policy_id: UUID = Field(
        ...,
        description="Policy record referenced by the audit event.",
        examples=["a9a36b83-fc50-451c-92c3-2e1f2d9a126f"],
    )
    request_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Correlation identifier for the audited request.",
        examples=["req_01J2Z7F3Q8EXAMPLE"],
    )
    action: AuditAction = Field(
        ...,
        description="Authorization workflow action that was audited.",
        examples=[AuditAction.POLICY_EVALUATION],
    )
    decision: AuditDecision = Field(
        ...,
        description="Decision captured for the audited action.",
        examples=[AuditDecision.RECONSENT_REQUIRED],
    )
    message: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional human-readable audit message.",
        examples=["Consent has expired and re-consent is required."],
    )
    timestamp: datetime = Field(
        ...,
        description="Timezone-aware timestamp when the audit event occurred.",
        examples=["2026-07-21T18:30:00+05:30"],
    )
