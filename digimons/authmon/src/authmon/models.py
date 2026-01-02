"""
Data models for authmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for authmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="authmon", description="Digimon name")
    auth_methods: List[str] = Field(
        default_factory=lambda: ["password", "mfa", "biometric"],
        description="Supported authentication methods",
    )
    max_attempts: int = Field(default=5, ge=1, description="Maximum authentication attempts")
    lockout_duration: int = Field(default=300, ge=1, description="Lockout duration in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


class AuthResult(BaseModel):
    """Result of authentication attempt"""

    success: bool = Field(description="Whether authentication succeeded")
    user_id: Optional[str] = Field(default=None, description="Authenticated user ID")
    method: str = Field(description="Authentication method used")
    timestamp: str = Field(description="Authentication timestamp")
    attempts_remaining: int = Field(default=0, description="Remaining attempts")
    locked: bool = Field(default=False, description="Whether account is locked")
    errors: List[str] = Field(default_factory=list, description="Authentication errors")


class AnalysisResult(BaseModel):
    """Result model for analysis operations"""

    status: str = Field(description="Status of the analysis")
    message: str = Field(description="Descriptive message")
    data: Dict[str, Any] = Field(default_factory=dict, description="Result data")
    errors: Optional[List[str]] = Field(default=None, description="List of errors if any")


class DigimonInfo(BaseModel):
    """Information model for Digimon metadata"""

    name: str
    mission: str
    role: str
    status: str
    auth_methods: str
    max_attempts: str
    version: str = "3.0.0"

