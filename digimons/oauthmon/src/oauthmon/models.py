"""
Data models for oauthmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for oauthmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="oauthmon", description="Digimon name")
    authorization_url: Optional[str] = Field(default=None, description="OAuth authorization URL")
    token_url: Optional[str] = Field(default=None, description="OAuth token URL")
    client_id: Optional[str] = Field(default=None, description="OAuth client ID")
    supported_flows: List[str] = Field(
        default_factory=lambda: ["authorization_code", "client_credentials", "implicit"],
        description="Supported OAuth flows",
    )
    debug: bool = Field(default=False, description="Enable debug mode")


class OAuthToken(BaseModel):
    """OAuth token information"""

    access_token: str = Field(description="Access token")
    token_type: str = Field(default="Bearer", description="Token type")
    expires_in: Optional[int] = Field(default=None, description="Expiration time in seconds")
    refresh_token: Optional[str] = Field(default=None, description="Refresh token")
    scope: Optional[str] = Field(default=None, description="Token scope")
    created_at: str = Field(description="Token creation timestamp")


class OAuthAnalysis(BaseModel):
    """Result of OAuth analysis"""

    total_tokens: int = Field(description="Total OAuth tokens")
    active_tokens: int = Field(description="Number of active tokens")
    tokens_by_flow: Dict[str, int] = Field(default_factory=dict, description="Tokens by flow type")
    expired_tokens: int = Field(default=0, description="Number of expired tokens")
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
    supported_flows: str
    client_id: str
    version: str = "3.0.0"

