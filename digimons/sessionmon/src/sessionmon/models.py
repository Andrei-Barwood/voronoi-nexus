"""
Data models for sessionmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for sessionmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="sessionmon", description="Digimon name")
    session_timeout: int = Field(default=3600, ge=60, description="Session timeout in seconds")
    max_concurrent_sessions: int = Field(default=10, ge=1, description="Max concurrent sessions per user")
    enable_session_fixation: bool = Field(default=True, description="Enable session fixation protection")
    debug: bool = Field(default=False, description="Enable debug mode")


class Session(BaseModel):
    """Session information"""

    session_id: str = Field(description="Unique session identifier")
    user_id: str = Field(description="User ID")
    created_at: str = Field(description="Session creation timestamp")
    expires_at: str = Field(description="Session expiration timestamp")
    last_activity: str = Field(description="Last activity timestamp")
    ip_address: Optional[str] = Field(default=None, description="IP address")
    user_agent: Optional[str] = Field(default=None, description="User agent")


class SessionAnalysis(BaseModel):
    """Result of session analysis"""

    total_sessions: int = Field(description="Total active sessions")
    active_sessions: int = Field(description="Number of active sessions")
    expired_sessions: int = Field(description="Number of expired sessions")
    sessions_by_user: Dict[str, int] = Field(default_factory=dict, description="Sessions per user")
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
    session_timeout: str
    max_concurrent_sessions: str
    version: str = "3.0.0"

