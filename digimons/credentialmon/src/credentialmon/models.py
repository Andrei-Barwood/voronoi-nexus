"""
Data models for credentialmon (Mega).

Define Pydantic models for type validation and documentation.
"""

import base64
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for credentialmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="credentialmon", description="Digimon name")
    encryption_enabled: bool = Field(default=True, description="Enable encryption for credentials")
    key_rotation_days: int = Field(default=90, ge=1, description="Key rotation interval in days")
    hash_algorithm: str = Field(default="sha256", description="Hashing algorithm")
    debug: bool = Field(default=False, description="Enable debug mode")


class Credential(BaseModel):
    """Credential information"""

    credential_id: str = Field(description="Unique credential identifier")
    username: Optional[str] = Field(default=None, description="Username")
    service: str = Field(description="Service/application name")
    encrypted: bool = Field(default=True, description="Whether credential is encrypted")
    created_at: str = Field(description="Creation timestamp")
    last_rotated: Optional[str] = Field(default=None, description="Last rotation timestamp")


class CredentialVault(BaseModel):
    """Credential vault analysis"""

    total_credentials: int = Field(description="Total credentials stored")
    encrypted_count: int = Field(description="Number of encrypted credentials")
    unencrypted_count: int = Field(description="Number of unencrypted credentials")
    expired_keys: int = Field(default=0, description="Number of expired encryption keys")
    credentials: List[Credential] = Field(default_factory=list, description="List of credentials")
    vault_summary: Dict[str, Any] = Field(default_factory=dict, description="Vault summary")


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
    encryption_enabled: str
    key_rotation_days: str
    version: str = "3.0.0"

