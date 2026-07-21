"""FastAPI application entry point."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.database.database import verify_database_connection

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Verify external dependencies during application startup."""

    try:
        verify_database_connection()
        logger.info("PostgreSQL database connection verified successfully.")
    except ValueError as exc:
        logger.error("Application configuration error: %s", exc)
        raise RuntimeError("Invalid application configuration.") from exc
    except SQLAlchemyError as exc:
        logger.error("PostgreSQL database connection failed: %s", exc)
        raise RuntimeError("Database connectivity check failed.") from exc

    yield


app = FastAPI(
    title="Biometric Consent & Policy Enforcement Framework",
    version="0.1.0",
    description="Phase 1 backend skeleton for the Samsung PRISM project.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Return basic service health information."""

    return {
        "project": "Biometric Consent & Policy Enforcement Framework",
        "status": "Running",
    }
