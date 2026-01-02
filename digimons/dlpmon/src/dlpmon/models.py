"""
Data models for dlpmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for dlpmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="dlpmon", description="Digimon name")
    detection_modes: List[str] = Field(
        default_factory=lambda: ["content", "context", "behavior"],
        description="Detection modes enabled",
    )
    sensitivity_level: str = Field(default="medium", description="Sensitivity level (low/medium/high)")
    enable_blocking: bool = Field(default=True, description="Enable automatic blocking")
    alert_threshold: int = Field(default=3, ge=1, description="Alert threshold for violations")
    debug: bool = Field(default=False, description="Enable debug mode")


class PolicyViolation(BaseModel):
    """Policy violation information"""

    violation_id: str = Field(description="Unique violation identifier")
    policy_name: str = Field(description="Policy that was violated")
    violation_type: str = Field(description="Type of violation")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    detected_data: str = Field(description="Detected sensitive data")
    location: Optional[str] = Field(default=None, description="Location where violation occurred")
    timestamp: str = Field(description="Violation timestamp")


class DLPAnalysis(BaseModel):
    """Result of DLP analysis"""

    total_scanned: int = Field(description="Total items scanned")
    violations_detected: int = Field(description="Number of violations detected")
    violations_by_severity: Dict[str, int] = Field(default_factory=dict, description="Violations by severity")
    violations_by_policy: Dict[str, int] = Field(default_factory=dict, description="Violations by policy")
    violations: List[PolicyViolation] = Field(default_factory=list, description="List of violations")
    blocked_count: int = Field(default=0, description="Number of items blocked")
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
    detection_modes: str
    sensitivity_level: str
    version: str = "3.0.0"

