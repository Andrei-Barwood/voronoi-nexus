"""
Data models for anonymizemon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for anonymizemon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="anonymizemon", description="Digimon name")
    anonymization_method: str = Field(default="pseudonymize", description="Method (pseudonymize/generalize/randomize)")
    preserve_format: bool = Field(default=True, description="Preserve data format")
    reversible: bool = Field(default=False, description="Enable reversible anonymization")
    seed: Optional[str] = Field(default=None, description="Seed for deterministic anonymization")
    debug: bool = Field(default=False, description="Enable debug mode")


class AnonymizationRecord(BaseModel):
    """Record of an anonymization operation"""

    record_id: str = Field(description="Unique record identifier")
    field_name: str = Field(description="Field that was anonymized")
    original_value: str = Field(description="Original value")
    anonymized_value: str = Field(description="Anonymized value")
    method: str = Field(description="Anonymization method used")
    reversible: bool = Field(description="Whether anonymization is reversible")


class AnonymizationResult(BaseModel):
    """Result of anonymization operation"""

    original_data: Dict[str, Any] = Field(description="Original data")
    anonymized_data: Dict[str, Any] = Field(description="Anonymized data")
    total_fields: int = Field(description="Total fields processed")
    anonymized_fields: int = Field(description="Number of fields anonymized")
    anonymization_records: List[AnonymizationRecord] = Field(default_factory=list, description="List of anonymization records")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Anonymization statistics")


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
    anonymization_method: str
    reversible: str
    version: str = "3.0.0"

