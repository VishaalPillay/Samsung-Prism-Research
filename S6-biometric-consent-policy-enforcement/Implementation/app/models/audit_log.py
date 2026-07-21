"""Audit log ORM model for immutable authorization records."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, event, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, Mapper, mapped_column, relationship

from app.database.base import Base
from app.models.enums import AuditAction, AuditDecision, enum_values

if TYPE_CHECKING:
    from app.models.consent import Consent
    from app.models.policy import Policy


class AuditLog(Base):
    """Represents an immutable authorization audit record."""

    __tablename__ = "audit_logs"

    audit_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    consent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("consents.consent_id", ondelete="RESTRICT"),
        nullable=False,
    )
    policy_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("policies.policy_id", ondelete="RESTRICT"),
        nullable=False,
    )
    request_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    action: Mapped[AuditAction] = mapped_column(
        Enum(
            AuditAction,
            name="audit_action_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
    )
    decision: Mapped[AuditDecision] = mapped_column(
        Enum(
            AuditDecision,
            name="audit_decision_enum",
            native_enum=True,
            validate_strings=True,
            values_callable=enum_values,
        ),
        nullable=False,
    )
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )

    consent: Mapped["Consent"] = relationship(back_populates="audit_logs")
    policy: Mapped["Policy"] = relationship(back_populates="audit_logs")

    __table_args__ = (
        Index("ix_audit_logs_user_timestamp", "user_id", "timestamp"),
        Index("ix_audit_logs_consent_id", "consent_id"),
        Index("ix_audit_logs_policy_id", "policy_id"),
        Index("ix_audit_logs_action_decision", "action", "decision"),
    )


@event.listens_for(AuditLog, "before_update", propagate=True)
def prevent_audit_log_update(
    mapper: Mapper[AuditLog],
    connection: Connection,
    target: AuditLog,
) -> None:
    """Prevent ORM updates to immutable audit records."""

    raise ValueError("AuditLog records are immutable and cannot be updated.")


@event.listens_for(AuditLog, "before_delete", propagate=True)
def prevent_audit_log_delete(
    mapper: Mapper[AuditLog],
    connection: Connection,
    target: AuditLog,
) -> None:
    """Prevent ORM deletes of immutable audit records."""

    raise ValueError("AuditLog records are immutable and cannot be deleted.")
