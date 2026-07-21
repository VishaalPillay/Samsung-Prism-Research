"""SQLAlchemy database engine, sessions, and connectivity checks."""

from collections.abc import Generator
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import validate_startup_settings
from app.database.base import Base


@lru_cache
def get_engine(database_url: str) -> Engine:
    """Create and cache the SQLAlchemy engine."""

    return create_engine(
        database_url,
        pool_pre_ping=True,
    )


@lru_cache
def get_session_local(database_url: str) -> sessionmaker[Session]:
    """Create and cache the SQLAlchemy session factory."""

    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine(database_url),
        expire_on_commit=False,
    )


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for request-scoped usage."""

    settings = validate_startup_settings()
    db = get_session_local(settings.database_url)()
    try:
        yield db
    finally:
        db.close()


def verify_database_connection() -> None:
    """Verify PostgreSQL connectivity with a lightweight query."""

    settings = validate_startup_settings()

    with get_engine(settings.database_url).connect() as connection:
        connection.execute(text("SELECT 1"))
