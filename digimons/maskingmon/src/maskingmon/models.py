"""
Data models for maskingmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for maskingmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="maskingmon", description="Digimon name")
    mask_character: str = Field(default="*", description="Character used for masking")
    mask_length: Optional[int] = Field(default=None, description="Fixed mask length (None = preserve original length)")
    preserve_format: bool = Field(default=True, description="Preserve data format")
    pii_types: List[str] = Field(
        default_factory=lambda: ["email", "phone", "credit_card", "ssn", "ip"],
        description="PII types to mask",
    )
    log_context: bool = Field(default=True, description="Include context in log masking")
    debug: bool = Field(default=False, description="Enable debug mode")


class MaskingRecord(BaseModel):
    """Record of a masking operation"""

    record_id: str = Field(description="Unique record identifier")
    pii_type: str = Field(description="Type of PII masked")
    original_value: str = Field(description="Original value")
    masked_value: str = Field(description="Masked value")
    position: int = Field(description="Position in text")
    preserve_format: bool = Field(description="Whether format was preserved")


class MaskingResult(BaseModel):
    """Result of masking operation"""

    original_text: str = Field(description="Original text")
    masked_text: str = Field(description="Text with masked PII")
    total_masked: int = Field(description="Total number of items masked")
    masked_by_type: Dict[str, int] = Field(default_factory=dict, description="Masked items by type")
    masking_records: List[MaskingRecord] = Field(default_factory=list, description="List of masking records")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Masking statistics")


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
    mask_character: str
    pii_types: str
    version: str = "3.0.0"

