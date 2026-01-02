"""
Data models for privacymon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for privacymon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="privacymon", description="Digimon name")
    strict_mode: bool = Field(default=True, description="Enable strict privacy policy checking")
    check_data_collection: bool = Field(default=True, description="Check data collection practices")
    check_data_sharing: bool = Field(default=True, description="Check data sharing practices")
    check_user_rights: bool = Field(default=True, description="Check user privacy rights")
    debug: bool = Field(default=False, description="Enable debug mode")


class PrivacyCheck(BaseModel):
    """Individual privacy policy check result"""

    check_id: str = Field(description="Unique check identifier")
    policy_area: str = Field(description="Policy area being checked")
    requirement: str = Field(description="Requirement description")
    status: str = Field(description="Check status (pass/fail/warning)")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    description: str = Field(description="Check description")
    remediation: Optional[str] = Field(default=None, description="Remediation steps")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence data")


class PrivacyAudit(BaseModel):
    """Privacy policy audit result"""

    audit_id: str = Field(description="Unique audit identifier")
    total_checks: int = Field(description="Total number of checks")
    passed_checks: int = Field(description="Number of passed checks")
    failed_checks: int = Field(description="Number of failed checks")
    warning_checks: int = Field(description="Number of warning checks")
    compliance_score: float = Field(ge=0.0, le=100.0, description="Overall compliance score")
    checks: List[PrivacyCheck] = Field(default_factory=list, description="List of privacy checks")
    privacy_policy_status: Dict[str, Any] = Field(default_factory=dict, description="Privacy policy status")
    summary: Dict[str, Any] = Field(default_factory=dict, description="Audit summary")


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
    strict_mode: str
    version: str = "3.0.0"

