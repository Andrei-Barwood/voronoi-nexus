"""
Data models for thirstmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for thirstmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="thirstmon", description="Digimon name")
    threat_types: List[str] = Field(
        default_factory=lambda: ["ip", "domain", "url", "hash", "email"],
        description="Types of IOCs to detect",
    )
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum confidence threshold")
    enable_reputation_check: bool = Field(default=True, description="Enable reputation checking")
    debug: bool = Field(default=False, description="Enable debug mode")


class IOCMatch(BaseModel):
    """IOC match information"""

    ioc: str = Field(description="Indicator of Compromise")
    ioc_type: str = Field(description="Type of IOC (ip/domain/url/hash/email)")
    threat_category: str = Field(description="Threat category")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    source: str = Field(description="Source of the IOC match")


class ThreatAnalysis(BaseModel):
    """Result of threat analysis"""

    total_scanned: int = Field(description="Total IOCs scanned")
    threats_detected: int = Field(description="Number of threats detected")
    clean_count: int = Field(description="Number of clean IOCs")
    matches: List[IOCMatch] = Field(default_factory=list, description="List of threat matches")
    threats_by_type: Dict[str, int] = Field(default_factory=dict, description="Threats by IOC type")
    threats_by_category: Dict[str, int] = Field(default_factory=dict, description="Threats by category")
    analysis_summary: Dict[str, Any] = Field(default_factory=dict, description="Analysis summary")


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
    threat_types: str
    confidence_threshold: str
    version: str = "3.0.0"
