"""
Data models for mfamon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for mfamon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="mfamon", description="Digimon name")
    mfa_methods: List[str] = Field(
        default_factory=lambda: ["totp", "sms", "email", "push"],
        description="Supported MFA methods",
    )
    default_method: str = Field(default="totp", description="Default MFA method")
    code_expiry: int = Field(default=300, ge=60, description="Code expiry in seconds")
    max_attempts: int = Field(default=3, ge=1, description="Maximum verification attempts")
    debug: bool = Field(default=False, description="Enable debug mode")


class MFAChallenge(BaseModel):
    """MFA challenge information"""

    challenge_id: str = Field(description="Unique challenge identifier")
    user_id: str = Field(description="User ID")
    method: str = Field(description="MFA method used")
    code: Optional[str] = Field(default=None, description="Generated code (for testing)")
    expires_at: str = Field(description="Expiration timestamp")
    verified: bool = Field(default=False, description="Whether challenge was verified")
    attempts: int = Field(default=0, description="Verification attempts")


class MFAAnalysis(BaseModel):
    """Result of MFA analysis"""

    total_challenges: int = Field(description="Total MFA challenges")
    verified_count: int = Field(description="Number of verified challenges")
    pending_count: int = Field(description="Number of pending challenges")
    failed_count: int = Field(description="Number of failed challenges")
    methods_usage: Dict[str, int] = Field(default_factory=dict, description="Usage by method")
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
    mfa_methods: str
    default_method: str
    version: str = "3.0.0"

