"""
Data models for policymon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for policymon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="policymon", description="Digimon name")
    strict_mode: bool = Field(default=True, description="Enable strict policy enforcement")
    check_permissions: bool = Field(default=True, description="Check file permissions")
    check_encryption: bool = Field(default=True, description="Check encryption requirements")
    debug: bool = Field(default=False, description="Enable debug mode")


class PolicyCheck(BaseModel):
    """Result of a policy check"""

    policy_name: str = Field(description="Name of the policy being checked")
    compliant: bool = Field(description="Whether the check passed")
    violations: List[str] = Field(default_factory=list, description="List of violations")
    warnings: List[str] = Field(default_factory=list, description="List of warnings")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


class PolicyAudit(BaseModel):
    """Result of policy audit"""

    total_checks: int = Field(description="Total policy checks performed")
    passed_checks: int = Field(description="Number of checks that passed")
    failed_checks: int = Field(description="Number of checks that failed")
    checks: List[PolicyCheck] = Field(default_factory=list, description="Individual check results")
    audit_summary: Dict[str, Any] = Field(default_factory=dict, description="Audit summary")


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
