"""Workflow execution models."""
import os
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class WorkflowAuthConfig(BaseModel):
    """Authentication configuration with support for multiple auth methods."""
    username: Optional[str] = Field(
        default=None,
        description="Username for password-based authentication"
    )
    password: Optional[str] = Field(
        default=None,
        description="Password for password-based authentication"
    )
    client_id: str = Field(
        default="codemie-sdk",
        description="Client ID for authentication"
    )
    client_secret: Optional[str] = Field(
        default=None,
        description="Client secret for client credentials"
    )

    @model_validator(mode="after")
    def validate_auth_method(self) -> "WorkflowAuthConfig":
        """Validates that either username/password or client credentials are provided."""
        has_user_pass = bool(self.username and self.password)
        has_client_creds = bool(self.client_id and self.client_secret)

        if not (has_user_pass or has_client_creds):
            raise ValueError(
                "Authentication configuration missing. Please provide either:\n"
                "- CODEMIE_USERNAME and CODEMIE_PASSWORD for password authentication\n"
                "- CODEMIE_AUTH_CLIENT_ID and CODEMIE_AUTH_CLIENT_SECRET for client credentials"
            )
        return self


REQUIRED_SETTINGS = (
    "CODEMIE_AUTH_SERVER_URL",
    "CODEMIE_AUTH_REALM_NAME",
    "CODEMIE_API_DOMAIN",
)

_TRUE_VALUES = ("", "true", "1", "yes", "on")
_FALSE_VALUES = ("false", "0", "no", "off")


def _read_required_settings() -> dict:
    """Returns the required settings; raises one ValueError naming every missing one."""
    values = {name: os.environ.get(name, "").strip() for name in REQUIRED_SETTINGS}
    missing = [name for name, value in values.items() if not value]
    if missing:
        raise ValueError("Missing required settings: " + ", ".join(missing))
    return values


def _read_verify_ssl() -> bool:
    """Parses CODEMIE_VERIFY_SSL strictly; TLS verification stays on unless disabled explicitly."""
    value = os.environ.get("CODEMIE_VERIFY_SSL", "").strip().lower()
    if value in _TRUE_VALUES:
        return True
    if value in _FALSE_VALUES:
        return False
    raise ValueError(
        "Invalid value for CODEMIE_VERIFY_SSL: use true or false"
    )


class WorkflowSettings:
    """Application settings configured via environment variables."""
    # Default values as class variables
    DEFAULT_AUTH_CLIENT_ID = "codemie-sdk"

    auth: WorkflowAuthConfig
    api_domain: str
    auth_realm_name: str
    auth_server_url: str
    verify_ssl: bool = True

    def __init__(self):
        required = _read_required_settings()
        # Authentication settings
        self.auth = WorkflowAuthConfig(
            username=os.environ.get("CODEMIE_USERNAME"),
            password=os.environ.get("CODEMIE_PASSWORD"),
            client_id=os.environ.get(
                "CODEMIE_AUTH_CLIENT_ID", self.DEFAULT_AUTH_CLIENT_ID
            ),
            client_secret=os.environ.get("CODEMIE_AUTH_CLIENT_SECRET"),
        )

        # Server configuration
        self.auth_client_id = os.environ.get(
            "CODEMIE_AUTH_CLIENT_ID", self.DEFAULT_AUTH_CLIENT_ID
        )
        self.auth_realm_name = required["CODEMIE_AUTH_REALM_NAME"]
        self.auth_server_url = required["CODEMIE_AUTH_SERVER_URL"]
        self.api_domain = required["CODEMIE_API_DOMAIN"]
        self.verify_ssl = _read_verify_ssl()


class WorkflowExecutionStatus(str, Enum):
    """Status of workflow execution"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    SUCCEEDED = "Succeeded"
    FAILED = "Failed"
    INTERRUPTED = "Interrupted"
    ABORTED = "Aborted"


class WorkflowExecutionResponse(BaseModel):
    """Response model for workflow execution"""
    id: str = Field(..., description="Unique identifier of the workflow")
    execution_id: str = Field(..., description="Unique identifier of the execution")
    workflow_id: str = Field(..., description="ID of the executed workflow")
    status: WorkflowExecutionStatus = Field(
        ..., 
        alias="overall_status",
        description="Current execution status"
    )
    created_date: datetime = Field(
        ..., 
        alias="date",
        description="Execution creation timestamp"
    )
    prompt: str = Field(..., description="User input/prompt for the execution")
    updated_date: Optional[datetime] = Field(None, description="Last update timestamp")
    
    class Config:
        populate_by_name = True


class WorkflowExecutionRequest(BaseModel):
    """Request model for workflow execution"""
    workflow_id: str = Field(..., description="ID of the workflow to execute")
    user_input: str = Field(
        default="",
        description="Optional user input/prompt for the workflow"
    )