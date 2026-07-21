"""Pydantic schemas for biometric authorization policies."""

from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.common import SchemaBase
from app.schemas.enums import BiometricType, ConsentPurpose, PolicyEffect


class PolicyCreate(SchemaBase):
    """Schema for creating an authorization policy."""

    policy_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Unique human-readable policy name.",
        examples=["Allow face authentication"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional policy description.",
        examples=["Allows face biometrics for authentication workflows."],
    )
    biometric_type: BiometricType = Field(
        ...,
        description="Biometric modality matched by the policy.",
        examples=[BiometricType.FACE],
    )
    purpose: ConsentPurpose = Field(
        ...,
        description="Processing purpose matched by the policy.",
        examples=[ConsentPurpose.AUTHENTICATION],
    )
    effect: PolicyEffect = Field(
        ...,
        description="Authorization effect produced by the policy.",
        examples=[PolicyEffect.ALLOW],
    )
    priority: int = Field(
        default=0,
        ge=0,
        description="Policy priority; higher values are evaluated first.",
        examples=[100],
    )
    enabled: bool = Field(
        default=True,
        description="Whether the policy is active for evaluation.",
        examples=[True],
    )


class PolicyUpdate(SchemaBase):
    """Schema for updating authorization policy metadata."""

    policy_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Unique human-readable policy name.",
        examples=["Deny expired iris access"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional policy description.",
        examples=["Blocks iris biometrics for expired consent contexts."],
    )
    biometric_type: BiometricType | None = Field(
        default=None,
        description="Biometric modality matched by the policy.",
        examples=[BiometricType.IRIS],
    )
    purpose: ConsentPurpose | None = Field(
        default=None,
        description="Processing purpose matched by the policy.",
        examples=[ConsentPurpose.ACCESS_CONTROL],
    )
    effect: PolicyEffect | None = Field(
        default=None,
        description="Authorization effect produced by the policy.",
        examples=[PolicyEffect.DENY],
    )
    priority: int | None = Field(
        default=None,
        ge=0,
        description="Policy priority; higher values are evaluated first.",
        examples=[50],
    )
    enabled: bool | None = Field(
        default=None,
        description="Whether the policy is active for evaluation.",
        examples=[False],
    )


class PolicyResponse(SchemaBase):
    """Schema returned for authorization policy records."""

    policy_id: UUID = Field(
        ...,
        description="Unique policy identifier.",
        examples=["a9a36b83-fc50-451c-92c3-2e1f2d9a126f"],
    )
    policy_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Unique human-readable policy name.",
        examples=["Allow face authentication"],
    )
    description: str | None = Field(
        default=None,
        max_length=2000,
        description="Optional policy description.",
        examples=["Allows face biometrics for authentication workflows."],
    )
    biometric_type: BiometricType = Field(
        ...,
        description="Biometric modality matched by the policy.",
        examples=[BiometricType.FACE],
    )
    purpose: ConsentPurpose = Field(
        ...,
        description="Processing purpose matched by the policy.",
        examples=[ConsentPurpose.AUTHENTICATION],
    )
    effect: PolicyEffect = Field(
        ...,
        description="Authorization effect produced by the policy.",
        examples=[PolicyEffect.ALLOW],
    )
    priority: int = Field(
        ...,
        ge=0,
        description="Policy priority; higher values are evaluated first.",
        examples=[100],
    )
    enabled: bool = Field(
        ...,
        description="Whether the policy is active for evaluation.",
        examples=[True],
    )
    created_at: datetime = Field(
        ...,
        description="Timezone-aware policy creation timestamp.",
        examples=["2026-07-21T18:30:00+05:30"],
    )
    updated_at: datetime = Field(
        ...,
        description="Timezone-aware timestamp of the latest policy update.",
        examples=["2026-07-21T18:30:00+05:30"],
    )
