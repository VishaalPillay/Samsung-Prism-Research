"""Consent ORM model for biometric consent records."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import (
    BiometricType,
    ConsentPurpose,
    ConsentStatus,
    enum_values,
)

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog


class Consent(Base):
    """Represents a user's biometric consent grant."""

    __tablename__ = "consents"

    consent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    biometric_type: Mapped[BiometricType] = mapped_column(
        Enum(
            BiometricType,
            name="biometric_type_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
    )
    purpose: Mapped[ConsentPurpose] = mapped_column(
        Enum(
            ConsentPurpose,
            name="consent_purpose_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
    )
    status: Mapped[ConsentStatus] = mapped_column(
        Enum(
            ConsentStatus,
            name="consent_status_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
        index=True,
    )
    consent_version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="consent",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_consents_user_status", "user_id", "status"),
        Index(
            "ix_consents_biometric_purpose_status",
            "biometric_type",
            "purpose",
            "status",
        ),
        Index("ix_consents_expires_at", "expires_at"),
    )
