"""
Data models for identitymon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for identitymon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="identitymon", description="Digimon name")
    validate_attributes: bool = Field(default=True, description="Validate identity attributes")
    check_roles: bool = Field(default=True, description="Check role assignments")
    enforce_policies: bool = Field(default=True, description="Enforce identity policies")
    debug: bool = Field(default=False, description="Enable debug mode")


class Identity(BaseModel):
    """Identity information"""

    user_id: str = Field(description="Unique user identifier")
    username: str = Field(description="Username")
    email: Optional[str] = Field(default=None, description="Email address")
    roles: List[str] = Field(default_factory=list, description="Assigned roles")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="Additional attributes")
    status: str = Field(default="active", description="Identity status")


class IdentityAnalysis(BaseModel):
    """Result of identity analysis"""

    total_identities: int = Field(description="Total identities processed")
    active_identities: int = Field(description="Number of active identities")
    inactive_identities: int = Field(description="Number of inactive identities")
    roles_distribution: Dict[str, int] = Field(default_factory=dict, description="Roles distribution")
    policy_violations: List[str] = Field(default_factory=list, description="Policy violations found")
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
    validate_attributes: str
    version: str = "3.0.0"

