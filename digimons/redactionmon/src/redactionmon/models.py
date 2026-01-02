"""
Data models for redactionmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for redactionmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="redactionmon", description="Digimon name")
    redaction_style: str = Field(default="mask", description="Redaction style (mask/tokenize/remove)")
    preserve_structure: bool = Field(default=True, description="Preserve document structure")
    pii_types: List[str] = Field(
        default_factory=lambda: ["email", "phone", "ssn", "credit_card", "ip"],
        description="PII types to redact",
    )
    debug: bool = Field(default=False, description="Enable debug mode")


class RedactionRecord(BaseModel):
    """Record of a redaction operation"""

    record_id: str = Field(description="Unique record identifier")
    pii_type: str = Field(description="Type of PII redacted")
    original_value: str = Field(description="Original value (truncated)")
    redacted_value: str = Field(description="Redacted value")
    position: int = Field(description="Position in document")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")


class RedactionResult(BaseModel):
    """Result of redaction operation"""

    original_text: str = Field(description="Original text")
    redacted_text: str = Field(description="Text with redacted PII")
    total_redactions: int = Field(description="Total number of redactions")
    redactions_by_type: Dict[str, int] = Field(default_factory=dict, description="Redactions by PII type")
    redaction_records: List[RedactionRecord] = Field(default_factory=list, description="List of redaction records")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Redaction statistics")


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
    redaction_style: str
    pii_types: str
    version: str = "3.0.0"

