"""Common reusable Pydantic response schemas."""

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    """Base schema configured for SQLAlchemy attribute parsing."""

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(SchemaBase):
    """Generic message response schema."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Human-readable operation result message.",
        examples=["Operation completed successfully"],
    )


class HealthResponse(SchemaBase):
    """Application health response schema."""

    status: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Current application status.",
        examples=["Running"],
    )


class ErrorResponse(SchemaBase):
    """Generic error response schema."""

    detail: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Human-readable error detail.",
        examples=["Invalid request payload"],
    )
