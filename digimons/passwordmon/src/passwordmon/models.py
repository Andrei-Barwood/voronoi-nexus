"""
Data models for passwordmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for passwordmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="passwordmon", description="Digimon name")
    min_length: int = Field(default=12, ge=8, description="Minimum password length")
    require_uppercase: bool = Field(default=True, description="Require uppercase letters")
    require_lowercase: bool = Field(default=True, description="Require lowercase letters")
    require_numbers: bool = Field(default=True, description="Require numbers")
    require_special: bool = Field(default=True, description="Require special characters")
    check_common_passwords: bool = Field(default=True, description="Check against common passwords")
    debug: bool = Field(default=False, description="Enable debug mode")


class PasswordValidation(BaseModel):
    """Result of password validation"""

    password: str = Field(description="Password being validated")
    valid: bool = Field(description="Whether password is valid")
    strength: str = Field(description="Password strength (weak/medium/strong)")
    score: int = Field(default=0, ge=0, le=100, description="Password strength score (0-100)")
    violations: List[str] = Field(default_factory=list, description="Validation violations")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


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
    min_length: str
    require_special: str
    version: str = "3.0.0"

