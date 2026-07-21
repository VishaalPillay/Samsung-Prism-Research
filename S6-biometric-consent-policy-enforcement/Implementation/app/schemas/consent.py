"""Pydantic schemas for biometric consent data transfer."""

from datetime import datetime
from uuid import UUID

from pydantic import Field, FutureDatetime

from app.schemas.common import SchemaBase
from app.schemas.enums import BiometricType, ConsentPurpose, ConsentStatus


class ConsentCreate(SchemaBase):
    """Schema for creating a biometric consent record."""

    user_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="External identity of the user granting consent.",
        examples=["user_12345"],
    )
    biometric_type: BiometricType = Field(
        ...,
        description="Biometric modality covered by the consent.",
        examples=[BiometricType.FACE],
    )
    purpose: ConsentPurpose = Field(
        ...,
        description="Purpose for which biometric data may be processed.",
        examples=[ConsentPurpose.AUTHENTICATION],
    )
    expires_at: FutureDatetime = Field(
        ...,
        description="Future timezone-aware consent expiration timestamp.",
        examples=["2027-07-21T18:30:00+05:30"],
    )


class ConsentUpdate(SchemaBase):
    """Schema for updating mutable consent fields."""

    expires_at: FutureDatetime | None = Field(
        default=None,
        description="Future timezone-aware consent expiration timestamp.",
        examples=["2027-07-21T18:30:00+05:30"],
    )
    status: ConsentStatus | None = Field(
        default=None,
        description="Updated lifecycle status for the consent.",
        examples=[ConsentStatus.REVOKED],
    )


class ConsentResponse(SchemaBase):
    """Schema returned for biometric consent records."""

    consent_id: UUID = Field(
        ...,
        description="Unique consent identifier.",
        examples=["7b9f0b9f-d3a1-4c2c-b7a1-0b0a4f7f9c10"],
    )
    user_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="External identity of the user who granted consent.",
        examples=["user_12345"],
    )
    biometric_type: BiometricType = Field(
        ...,
        description="Biometric modality covered by the consent.",
        examples=[BiometricType.FINGERPRINT],
    )
    purpose: ConsentPurpose = Field(
        ...,
        description="Purpose for which biometric data may be processed.",
        examples=[ConsentPurpose.ACCESS_CONTROL],
    )
    status: ConsentStatus = Field(
        ...,
        description="Current lifecycle status of the consent.",
        examples=[ConsentStatus.ACTIVE],
    )
    consent_version: int = Field(
        ...,
        ge=1,
        description="Version number of the consent record.",
        examples=[1],
    )
    created_at: datetime = Field(
        ...,
        description="Timezone-aware consent creation timestamp.",
        examples=["2026-07-21T18:30:00+05:30"],
    )
    updated_at: datetime = Field(
        ...,
        description="Timezone-aware timestamp of the latest consent update.",
        examples=["2026-07-21T18:30:00+05:30"],
    )
    expires_at: datetime = Field(
        ...,
        description="Timezone-aware consent expiration timestamp.",
        examples=["2027-07-21T18:30:00+05:30"],
    )
    revoked_at: datetime | None = Field(
        default=None,
        description="Timezone-aware revocation timestamp when revoked.",
        examples=[None],
    )
