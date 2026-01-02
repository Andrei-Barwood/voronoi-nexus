"""
Data models for forensimon (Mega).

Define Pydantic models for type validation and documentation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for forensimon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="forensimon", description="Digimon name")
    max_file_size_mb: int = Field(default=100, ge=1, description="Maximum file size in MB")
    supported_formats: List[str] = Field(
        default_factory=lambda: [".log", ".txt", ".json", ".csv", ".xml"],
        description="Supported file formats",
    )
    extract_timestamps: bool = Field(default=True, description="Extract timestamps from logs")
    extract_ips: bool = Field(default=True, description="Extract IP addresses")
    extract_emails: bool = Field(default=True, description="Extract email addresses")
    debug: bool = Field(default=False, description="Enable debug mode")


class ArtifactAnalysis(BaseModel):
    """Result of artifact analysis"""

    artifact_path: str = Field(description="Path to analyzed artifact")
    artifact_type: str = Field(description="Type of artifact (log, file, etc)")
    file_size: int = Field(default=0, description="File size in bytes")
    line_count: int = Field(default=0, description="Number of lines")
    timestamps_found: List[str] = Field(default_factory=list, description="Timestamps extracted")
    ips_found: List[str] = Field(default_factory=list, description="IP addresses found")
    emails_found: List[str] = Field(default_factory=list, description="Email addresses found")
    suspicious_patterns: List[str] = Field(default_factory=list, description="Suspicious patterns detected")
    analysis_summary: Dict[str, Any] = Field(default_factory=dict, description="Summary statistics")


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
    max_file_size_mb: str
    supported_formats: str
    version: str = "3.0.0"
