"""Initial schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-07-21 18:45:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


biometric_type_enum = postgresql.ENUM(
    "FACE",
    "FINGERPRINT",
    "IRIS",
    "VOICE",
    name="biometric_type_enum",
)
consent_purpose_enum = postgresql.ENUM(
    "Authentication",
    "Identity Verification",
    "Access Control",
    name="consent_purpose_enum",
)
consent_status_enum = postgresql.ENUM(
    "ACTIVE",
    "REVOKED",
    "EXPIRED",
    name="consent_status_enum",
)
policy_effect_enum = postgresql.ENUM(
    "ALLOW",
    "DENY",
    name="policy_effect_enum",
)
audit_action_enum = postgresql.ENUM(
    "CONSENT_CHECK",
    "POLICY_EVALUATION",
    "AUTHORIZATION",
    name="audit_action_enum",
)
audit_decision_enum = postgresql.ENUM(
    "ALLOW",
    "DENY",
    "RECONSENT_REQUIRED",
    name="audit_decision_enum",
)


def upgrade() -> None:
    """Create initial biometric consent policy tables."""

    bind = op.get_bind()
    biometric_type_enum.create(bind, checkfirst=True)
    consent_purpose_enum.create(bind, checkfirst=True)
    consent_status_enum.create(bind, checkfirst=True)
    policy_effect_enum.create(bind, checkfirst=True)
    audit_action_enum.create(bind, checkfirst=True)
    audit_decision_enum.create(bind, checkfirst=True)

    op.create_table(
        "consents",
        sa.Column("consent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.String(length=255), nullable=False),
        sa.Column(
            "biometric_type",
            biometric_type_enum,
            nullable=False,
        ),
        sa.Column("purpose", consent_purpose_enum, nullable=False),
        sa.Column("status", consent_status_enum, nullable=False),
        sa.Column("consent_version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("consent_id"),
    )
    op.create_index(
        "ix_consents_biometric_purpose_status",
        "consents",
        ["biometric_type", "purpose", "status"],
        unique=False,
    )
    op.create_index(
        "ix_consents_expires_at",
        "consents",
        ["expires_at"],
        unique=False,
    )
    op.create_index(
        "ix_consents_status",
        "consents",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_consents_user_id",
        "consents",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_consents_user_status",
        "consents",
        ["user_id", "status"],
        unique=False,
    )

    op.create_table(
        "policies",
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("policy_name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "biometric_type",
            biometric_type_enum,
            nullable=False,
        ),
        sa.Column("purpose", consent_purpose_enum, nullable=False),
        sa.Column("effect", policy_effect_enum, nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False),
        sa.Column(
            "enabled",
            sa.Boolean(),
            server_default="true",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("policy_id"),
    )
    op.create_index(
        "ix_policies_enabled_priority",
        "policies",
        ["enabled", sa.literal_column("priority DESC")],
        unique=False,
    )
    op.create_index(
        "ix_policies_match_priority",
        "policies",
        [
            "enabled",
            "biometric_type",
            "purpose",
            sa.literal_column("priority DESC"),
        ],
        unique=False,
    )
    op.create_index(
        "ix_policies_policy_name",
        "policies",
        ["policy_name"],
        unique=True,
    )
    op.create_table(
        "audit_logs",
        sa.Column("audit_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", sa.String(length=255), nullable=False),
        sa.Column("consent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("policy_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", sa.String(length=255), nullable=False),
        sa.Column("action", audit_action_enum, nullable=False),
        sa.Column("decision", audit_decision_enum, nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column(
            "timestamp",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["consent_id"],
            ["consents.consent_id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["policy_id"],
            ["policies.policy_id"],
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("audit_id"),
    )
    op.create_index(
        "ix_audit_logs_action_decision",
        "audit_logs",
        ["action", "decision"],
        unique=False,
    )
    op.create_index(
        "ix_audit_logs_consent_id",
        "audit_logs",
        ["consent_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_logs_policy_id",
        "audit_logs",
        ["policy_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_logs_request_id",
        "audit_logs",
        ["request_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_logs_timestamp",
        "audit_logs",
        ["timestamp"],
        unique=False,
    )
    op.create_index(
        "ix_audit_logs_user_id",
        "audit_logs",
        ["user_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_logs_user_timestamp",
        "audit_logs",
        ["user_id", "timestamp"],
        unique=False,
    )


def downgrade() -> None:
    """Drop initial biometric consent policy tables."""

    op.drop_index("ix_audit_logs_user_timestamp", table_name="audit_logs")
    op.drop_index("ix_audit_logs_user_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_timestamp", table_name="audit_logs")
    op.drop_index("ix_audit_logs_request_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_policy_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_consent_id", table_name="audit_logs")
    op.drop_index("ix_audit_logs_action_decision", table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index("ix_policies_policy_name", table_name="policies")
    op.drop_index("ix_policies_match_priority", table_name="policies")
    op.drop_index("ix_policies_enabled_priority", table_name="policies")
    op.drop_table("policies")

    op.drop_index("ix_consents_user_status", table_name="consents")
    op.drop_index("ix_consents_user_id", table_name="consents")
    op.drop_index("ix_consents_status", table_name="consents")
    op.drop_index("ix_consents_expires_at", table_name="consents")
    op.drop_index(
        "ix_consents_biometric_purpose_status",
        table_name="consents",
    )
    op.drop_table("consents")

    bind = op.get_bind()
    audit_decision_enum.drop(bind, checkfirst=True)
    audit_action_enum.drop(bind, checkfirst=True)
    policy_effect_enum.drop(bind, checkfirst=True)
    consent_status_enum.drop(bind, checkfirst=True)
    consent_purpose_enum.drop(bind, checkfirst=True)
    biometric_type_enum.drop(bind, checkfirst=True)
