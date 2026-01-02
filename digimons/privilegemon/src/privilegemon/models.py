"""
Data models for privilegemon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for privilegemon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="privilegemon", description="Digimon name")
    track_elevations: bool = Field(default=True, description="Track privilege elevations")
    require_justification: bool = Field(default=True, description="Require justification for elevation")
    max_elevation_duration: int = Field(default=3600, ge=60, description="Max elevation duration in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


class PrivilegeEvent(BaseModel):
    """Privilege elevation event"""

    event_id: str = Field(description="Unique event identifier")
    user_id: str = Field(description="User ID")
    requested_privilege: str = Field(description="Requested privilege level")
    justification: Optional[str] = Field(default=None, description="Justification for elevation")
    granted: bool = Field(description="Whether elevation was granted")
    timestamp: str = Field(description="Event timestamp")
    duration: Optional[int] = Field(default=None, description="Elevation duration in seconds")


class PrivilegeAudit(BaseModel):
    """Result of privilege audit"""

    total_events: int = Field(description="Total privilege events")
    granted_count: int = Field(description="Number of granted elevations")
    denied_count: int = Field(description="Number of denied elevations")
    events_by_user: Dict[str, int] = Field(default_factory=dict, description="Events per user")
    violations: List[str] = Field(default_factory=list, description="Security violations")
    audit_summary: Dict[str, Any] = Field(default_factory=dict, description="Audit summary")


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
    require_justification: str
    max_elevation_duration: str
    version: str = "3.0.0"

