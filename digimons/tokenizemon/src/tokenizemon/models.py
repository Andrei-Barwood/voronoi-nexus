"""
Data models for tokenizemon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for tokenizemon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="tokenizemon", description="Digimon name")
    token_format: str = Field(default="uuid", description="Token format (uuid/random/sequential)")
    preserve_format: bool = Field(default=True, description="Preserve original data format")
    token_mapping_backend: str = Field(default="memory", description="Token mapping backend (memory/file/database)")
    enable_detokenization: bool = Field(default=True, description="Enable detokenization")
    token_prefix: Optional[str] = Field(default=None, description="Optional token prefix")
    debug: bool = Field(default=False, description="Enable debug mode")


class TokenizationRecord(BaseModel):
    """Record of a tokenization operation"""

    record_id: str = Field(description="Unique record identifier")
    original_value: str = Field(description="Original value (truncated)")
    token: str = Field(description="Generated token")
    token_type: str = Field(description="Type of tokenized data")
    created_at: str = Field(description="Tokenization timestamp")
    reversible: bool = Field(description="Whether tokenization is reversible")


class TokenizationResult(BaseModel):
    """Result of tokenization operation"""

    original_data: str = Field(description="Original data")
    tokenized_data: str = Field(description="Data with tokens")
    total_tokens: int = Field(description="Total number of tokens generated")
    tokens_by_type: Dict[str, int] = Field(default_factory=dict, description="Tokens by type")
    tokenization_records: List[TokenizationRecord] = Field(default_factory=list, description="List of tokenization records")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Tokenization statistics")


class DetokenizationResult(BaseModel):
    """Result of detokenization operation"""

    token: str = Field(description="Token to detokenize")
    original_value: Optional[str] = Field(default=None, description="Original value (if found)")
    found: bool = Field(description="Whether token was found")
    message: str = Field(description="Detokenization message")


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
    token_format: str
    enable_detokenization: str
    version: str = "3.0.0"

