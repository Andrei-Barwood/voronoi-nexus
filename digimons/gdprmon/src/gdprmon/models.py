"""
Data models for gdprmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for gdprmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="gdprmon", description="Digimon name")
    strict_mode: bool = Field(default=True, description="Enable strict GDPR compliance checking")
    check_data_subject_rights: bool = Field(default=True, description="Check data subject rights compliance")
    check_data_breach_notification: bool = Field(default=True, description="Check data breach notification requirements")
    check_consent_management: bool = Field(default=True, description="Check consent management")
    debug: bool = Field(default=False, description="Enable debug mode")


class GDPRCheck(BaseModel):
    """Individual GDPR compliance check result"""

    check_id: str = Field(description="Unique check identifier")
    article: str = Field(description="GDPR article being checked")
    requirement: str = Field(description="Requirement description")
    status: str = Field(description="Check status (pass/fail/warning)")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    description: str = Field(description="Check description")
    remediation: Optional[str] = Field(default=None, description="Remediation steps")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence data")


class GDPRComplianceReport(BaseModel):
    """GDPR compliance report"""

    report_id: str = Field(description="Unique report identifier")
    total_checks: int = Field(description="Total number of checks")
    passed_checks: int = Field(description="Number of passed checks")
    failed_checks: int = Field(description="Number of failed checks")
    warning_checks: int = Field(description="Number of warning checks")
    compliance_score: float = Field(ge=0.0, le=100.0, description="Overall compliance score")
    checks: List[GDPRCheck] = Field(default_factory=list, description="List of GDPR checks")
    data_subject_rights_status: Dict[str, Any] = Field(default_factory=dict, description="Data subject rights status")
    summary: Dict[str, Any] = Field(default_factory=dict, description="Report summary")


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

