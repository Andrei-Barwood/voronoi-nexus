"""
Data models for bandidmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for bandidmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="bandidmon", description="Digimon name")
    redaction_mode: str = Field(default="mask", description="Redaction mode (mask/tokenize/remove)")
    preserve_format: bool = Field(default=True, description="Preserve original format when redacting")
    enable_ip_detection: bool = Field(default=True, description="Enable IP address detection")
    enable_ssn_detection: bool = Field(default=True, description="Enable SSN detection")
    enable_phone_detection: bool = Field(default=True, description="Enable phone number detection")
    debug: bool = Field(default=False, description="Enable debug mode")


class RedactionResult(BaseModel):
    """Result of data redaction"""

    original_text: str = Field(description="Original text")
    safe_text: str = Field(description="Text with redacted PII")
    redacted_items: List[Dict[str, Any]] = Field(default_factory=list, description="List of redacted items with details")
    statistics: Dict[str, int] = Field(default_factory=dict, description="Statistics by PII type")
    total_redacted: int = Field(default=0, description="Total number of items redacted")


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
    redaction_mode: str
    supported_types: str
    version: str = "3.0.0"
