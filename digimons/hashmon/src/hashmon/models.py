"""
Data models for hashmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for hashmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="hashmon", description="Digimon name")
    default_algorithm: str = Field(default="sha256", description="Default hash algorithm")
    supported_algorithms: List[str] = Field(
        default_factory=lambda: ["md5", "sha1", "sha256", "sha512", "blake2b"],
        description="Supported hash algorithms",
    )
    enable_hmac: bool = Field(default=True, description="Enable HMAC verification")
    chunk_size: int = Field(default=8192, ge=1024, description="Chunk size for large files")
    debug: bool = Field(default=False, description="Enable debug mode")


class HashResult(BaseModel):
    """Hash computation result"""

    algorithm: str = Field(description="Hash algorithm used")
    hash_value: str = Field(description="Computed hash value (hex)")
    input_length: int = Field(description="Input length in bytes")
    computation_time_ms: float = Field(ge=0.0, description="Computation time in milliseconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class VerificationResult(BaseModel):
    """Hash verification result"""

    verified: bool = Field(description="Verification result")
    algorithm: str = Field(description="Hash algorithm used")
    expected_hash: str = Field(description="Expected hash value")
    computed_hash: str = Field(description="Computed hash value")
    match: bool = Field(description="Whether hashes match")
    message: str = Field(description="Verification message")


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
    supported_algorithms: str
    version: str = "3.0.0"

