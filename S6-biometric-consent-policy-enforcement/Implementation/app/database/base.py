"""Declarative SQLAlchemy base and model metadata registry."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""


from app.models.audit_log import AuditLog  # noqa: E402, F401
from app.models.consent import Consent  # noqa: E402, F401
from app.models.policy import Policy  # noqa: E402, F401
