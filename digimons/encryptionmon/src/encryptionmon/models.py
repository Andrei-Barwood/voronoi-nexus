"""
Data models for encryptionmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for encryptionmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="encryptionmon", description="Digimon name")
    default_algorithm: str = Field(default="AES-256-GCM", description="Default encryption algorithm")
    key_rotation_days: int = Field(default=90, ge=1, description="Key rotation interval in days")
    key_storage_backend: str = Field(default="memory", description="Key storage backend (memory/file/vault)")
    enable_key_derivation: bool = Field(default=True, description="Enable key derivation")
    debug: bool = Field(default=False, description="Enable debug mode")


class EncryptionKey(BaseModel):
    """Encryption key information"""

    key_id: str = Field(description="Unique key identifier")
    algorithm: str = Field(description="Encryption algorithm")
    key_type: str = Field(description="Key type (symmetric/asymmetric)")
    created_at: str = Field(description="Key creation timestamp")
    expires_at: Optional[str] = Field(default=None, description="Key expiration timestamp")
    rotation_count: int = Field(default=0, description="Number of rotations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Key metadata")


class KeyManagementResult(BaseModel):
    """Result of key management operation"""

    operation: str = Field(description="Operation performed (generate/rotate/revoke)")
    key_id: Optional[str] = Field(default=None, description="Key ID involved")
    success: bool = Field(description="Operation success status")
    message: str = Field(description="Operation message")
    keys_active: int = Field(description="Number of active keys")
    keys_rotated: int = Field(default=0, description="Number of keys rotated")
    keys_revoked: int = Field(default=0, description="Number of keys revoked")


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
    default_algorithm: str
    key_rotation_days: str
    version: str = "3.0.0"

