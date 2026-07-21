"""Policy ORM model for biometric authorization policies."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.enums import (
    BiometricType,
    ConsentPurpose,
    PolicyEffect,
    enum_values,
)

if TYPE_CHECKING:
    from app.models.audit_log import AuditLog


class Policy(Base):
    """Represents an authorization policy for biometric access decisions."""

    __tablename__ = "policies"

    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    policy_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
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
    effect: Mapped[PolicyEffect] = mapped_column(
        Enum(
            PolicyEffect,
            name="policy_effect_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
    )
    priority: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    enabled: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
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

    audit_logs: Mapped[list["AuditLog"]] = relationship(
        back_populates="policy",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_policies_enabled_priority", "enabled", priority.desc()),
        Index(
            "ix_policies_match_priority",
            "enabled",
            "biometric_type",
            "purpose",
            priority.desc(),
        ),
    )
