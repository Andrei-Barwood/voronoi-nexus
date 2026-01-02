"""
Data models for hipaamon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for hipaamon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="hipaamon", description="Digimon name")
    strict_mode: bool = Field(default=True, description="Enable strict HIPAA compliance checking")
    check_phi_protection: bool = Field(default=True, description="Check PHI protection requirements")
    check_access_controls: bool = Field(default=True, description="Check access control requirements")
    check_audit_logs: bool = Field(default=True, description="Check audit logging requirements")
    debug: bool = Field(default=False, description="Enable debug mode")


class HIPAACheck(BaseModel):
    """Individual HIPAA compliance check result"""

    check_id: str = Field(description="Unique check identifier")
    section: str = Field(description="HIPAA section being checked")
    requirement: str = Field(description="Requirement description")
    status: str = Field(description="Check status (pass/fail/warning)")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    description: str = Field(description="Check description")
    remediation: Optional[str] = Field(default=None, description="Remediation steps")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence data")


class HIPAAComplianceReport(BaseModel):
    """HIPAA compliance report"""

    report_id: str = Field(description="Unique report identifier")
    total_checks: int = Field(description="Total number of checks")
    passed_checks: int = Field(description="Number of passed checks")
    failed_checks: int = Field(description="Number of failed checks")
    warning_checks: int = Field(description="Number of warning checks")
    compliance_score: float = Field(ge=0.0, le=100.0, description="Overall compliance score")
    checks: List[HIPAACheck] = Field(default_factory=list, description="List of HIPAA checks")
    phi_protection_status: Dict[str, Any] = Field(default_factory=dict, description="PHI protection status")
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

