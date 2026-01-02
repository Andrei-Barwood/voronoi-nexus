"""
Data models for tokenmon (Mega).

Define Pydantic models for type validation and documentation.
"""

import base64
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for tokenmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="tokenmon", description="Digimon name")
    token_type: str = Field(default="JWT", description="Default token type")
    algorithm: str = Field(default="HS256", description="Default algorithm")
    expiration_hours: int = Field(default=24, ge=1, description="Default expiration in hours")
    secret_length: int = Field(default=32, ge=16, description="Secret key length in bytes")
    debug: bool = Field(default=False, description="Enable debug mode")


class TokenResult(BaseModel):
    """Result of token generation/validation"""

    token: Optional[str] = Field(default=None, description="Generated/validated token")
    token_type: str = Field(description="Token type")
    algorithm: str = Field(description="Algorithm used")
    expires_at: Optional[str] = Field(default=None, description="Expiration timestamp")
    valid: bool = Field(default=True, description="Whether token is valid")
    claims: Dict[str, Any] = Field(default_factory=dict, description="Token claims/payload")
    errors: List[str] = Field(default_factory=list, description="Validation errors")


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
    token_type: str
    algorithm: str
    version: str = "3.0.0"

