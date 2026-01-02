"""
Data models for compliancemon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for compliancemon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="compliancemon", description="Digimon name")
    compliance_frameworks: List[str] = Field(
        default_factory=lambda: ["GDPR", "HIPAA", "PCI-DSS", "SOX", "ISO27001"],
        description="Compliance frameworks to check",
    )
    strict_mode: bool = Field(default=True, description="Enable strict compliance checking")
    auto_remediation: bool = Field(default=False, description="Enable automatic remediation")
    report_format: str = Field(default="json", description="Report format (json/xml/html)")
    debug: bool = Field(default=False, description="Enable debug mode")


class ComplianceCheck(BaseModel):
    """Individual compliance check result"""

    check_id: str = Field(description="Unique check identifier")
    framework: str = Field(description="Compliance framework")
    requirement: str = Field(description="Requirement being checked")
    status: str = Field(description="Check status (pass/fail/warning)")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    description: str = Field(description="Check description")
    remediation: Optional[str] = Field(default=None, description="Remediation steps")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence data")


class ComplianceAudit(BaseModel):
    """Result of compliance audit"""

    audit_id: str = Field(description="Unique audit identifier")
    frameworks_checked: List[str] = Field(description="Frameworks checked")
    total_checks: int = Field(description="Total number of checks")
    passed_checks: int = Field(description="Number of passed checks")
    failed_checks: int = Field(description="Number of failed checks")
    warning_checks: int = Field(description="Number of warning checks")
    compliance_score: float = Field(ge=0.0, le=100.0, description="Overall compliance score")
    checks: List[ComplianceCheck] = Field(default_factory=list, description="List of compliance checks")
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
    compliance_frameworks: str
    strict_mode: str
    version: str = "3.0.0"

