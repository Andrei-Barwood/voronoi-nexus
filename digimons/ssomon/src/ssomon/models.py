"""
Data models for ssomon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for ssomon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="ssomon", description="Digimon name")
    idp_url: Optional[str] = Field(default=None, description="Identity Provider URL")
    sp_entity_id: Optional[str] = Field(default=None, description="Service Provider entity ID")
    enable_saml: bool = Field(default=True, description="Enable SAML support")
    enable_oidc: bool = Field(default=True, description="Enable OpenID Connect support")
    debug: bool = Field(default=False, description="Enable debug mode")


class SSOSession(BaseModel):
    """SSO session information"""

    session_id: str = Field(description="Unique SSO session identifier")
    user_id: str = Field(description="User ID")
    idp: str = Field(description="Identity Provider")
    protocol: str = Field(description="SSO protocol (SAML/OIDC)")
    created_at: str = Field(description="Session creation timestamp")
    expires_at: str = Field(description="Session expiration timestamp")
    attributes: Dict[str, Any] = Field(default_factory=dict, description="User attributes")


class SSOAnalysis(BaseModel):
    """Result of SSO analysis"""

    total_sessions: int = Field(description="Total SSO sessions")
    active_sessions: int = Field(description="Number of active sessions")
    sessions_by_protocol: Dict[str, int] = Field(default_factory=dict, description="Sessions by protocol")
    sessions_by_idp: Dict[str, int] = Field(default_factory=dict, description="Sessions by IdP")
    violations: List[str] = Field(default_factory=list, description="Security violations")
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
    enable_saml: str
    enable_oidc: str
    version: str = "3.0.0"

