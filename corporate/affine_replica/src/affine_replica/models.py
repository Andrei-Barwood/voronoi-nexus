"""
Data models for affine_replica (Production).
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ModuleConfig(BaseModel):
    """Configuration model for affine_replica"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="Affine Replica", description="Module name")
    severity_threshold: str = Field(default="medium", description="Minimum severity to report")
    confidence_threshold: float = Field(default=0.7, ge=0.0, le=1.0, description="Minimum confidence score")
    enable_enrichment: bool = Field(default=True, description="Enable contextual enrichment")
    debug: bool = Field(default=False, description="Enable debug mode")


class DetectionFinding(BaseModel):
    """Detection finding"""

    indicator: str = Field(description="Observed indicator")
    category: str = Field(description="Finding category")
    severity: str = Field(description="Severity level")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    recommendation: Optional[str] = Field(default=None, description="Recommended action")


class DetectionReport(BaseModel):
    """Result of specialized threat analysis"""

    total_checks: int = Field(description="Total checks executed")
    alerts_count: int = Field(description="Number of alerts generated")
    findings: List[DetectionFinding] = Field(default_factory=list, description="Detection findings")
    summary: Dict[str, Any] = Field(default_factory=dict, description="Execution summary")


class AnalysisResult(BaseModel):
    """Result model for analysis operations"""

    status: str = Field(description="Status of the analysis")
    message: str = Field(description="Descriptive message")
    data: Dict[str, Any] = Field(default_factory=dict, description="Result data")
    errors: Optional[List[str]] = Field(default=None, description="List of errors if any")


class ModuleInfo(BaseModel):
    """Information model for module metadata"""

    name: str
    mission: str
    role: str
    status: str
    severity_threshold: str
    confidence_threshold: str
    version: str = "3.0.0"
