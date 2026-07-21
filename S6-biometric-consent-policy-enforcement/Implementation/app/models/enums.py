"""Shared database enum definitions for biometric policy models."""

from enum import StrEnum
from typing import TypeVar

EnumType = TypeVar("EnumType", bound=StrEnum)


def enum_values(enum_type: type[EnumType]) -> list[str]:
    """Return enum values for SQLAlchemy PostgreSQL enum labels."""

    return [member.value for member in enum_type]


class BiometricType(StrEnum):
    """Supported biometric modalities."""

    FACE = "FACE"
    FINGERPRINT = "FINGERPRINT"
    IRIS = "IRIS"
    VOICE = "VOICE"


class ConsentPurpose(StrEnum):
    """Supported purposes for biometric data processing."""

    AUTHENTICATION = "Authentication"
    IDENTITY_VERIFICATION = "Identity Verification"
    ACCESS_CONTROL = "Access Control"


class ConsentStatus(StrEnum):
    """Lifecycle states for biometric consent."""

    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class PolicyEffect(StrEnum):
    """Authorization effect produced by a policy."""

    ALLOW = "ALLOW"
    DENY = "DENY"


class AuditAction(StrEnum):
    """Auditable authorization workflow actions."""

    CONSENT_CHECK = "CONSENT_CHECK"
    POLICY_EVALUATION = "POLICY_EVALUATION"
    AUTHORIZATION = "AUTHORIZATION"


class AuditDecision(StrEnum):
    """Authorization decisions captured in audit records."""

    ALLOW = "ALLOW"
    DENY = "DENY"
    RECONSENT_REQUIRED = "RECONSENT_REQUIRED"
