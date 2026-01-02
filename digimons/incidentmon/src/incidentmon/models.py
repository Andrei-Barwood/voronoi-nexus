"""
Data models for incidentmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for incidentmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="incidentmon", description="Digimon name")
    auto_contain: bool = Field(default=False, description="Automatically contain incidents")
    severity_threshold: str = Field(default="medium", description="Minimum severity to act")
    notification_enabled: bool = Field(default=False, description="Enable notifications")
    debug: bool = Field(default=False, description="Enable debug mode")


class IncidentAction(BaseModel):
    """Incident response action"""

    action_type: str = Field(description="Type of action (contain, isolate, notify, etc)")
    target: str = Field(description="Target of the action")
    status: str = Field(description="Status of the action")
    timestamp: str = Field(description="Action timestamp")


class IncidentResponse(BaseModel):
    """Result of incident response"""

    incident_id: str = Field(description="Unique incident identifier")
    severity: str = Field(description="Incident severity")
    status: str = Field(description="Response status")
    actions_taken: List[IncidentAction] = Field(default_factory=list, description="Actions performed")
    contained: bool = Field(default=False, description="Whether incident was contained")
    response_summary: Dict[str, Any] = Field(default_factory=dict, description="Response summary")


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
    auto_contain: str
    severity_threshold: str
    version: str = "3.0.0"
