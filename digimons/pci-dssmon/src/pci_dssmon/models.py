"""
Data models for pci_dssmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for pci_dssmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="pci_dssmon", description="Digimon name")
    strict_mode: bool = Field(default=True, description="Enable strict PCI-DSS compliance checking")
    check_card_data_protection: bool = Field(default=True, description="Check card data protection requirements")
    check_network_segmentation: bool = Field(default=True, description="Check network segmentation requirements")
    check_vulnerability_management: bool = Field(default=True, description="Check vulnerability management requirements")
    debug: bool = Field(default=False, description="Enable debug mode")


class PCI_DSSCheck(BaseModel):
    """Individual PCI-DSS compliance check result"""

    check_id: str = Field(description="Unique check identifier")
    requirement: str = Field(description="PCI-DSS requirement number")
    description: str = Field(description="Requirement description")
    status: str = Field(description="Check status (pass/fail/warning)")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    remediation: Optional[str] = Field(default=None, description="Remediation steps")
    evidence: Dict[str, Any] = Field(default_factory=dict, description="Evidence data")


class PCI_DSSComplianceReport(BaseModel):
    """PCI-DSS compliance report"""

    report_id: str = Field(description="Unique report identifier")
    total_checks: int = Field(description="Total number of checks")
    passed_checks: int = Field(description="Number of passed checks")
    failed_checks: int = Field(description="Number of failed checks")
    warning_checks: int = Field(description="Number of warning checks")
    compliance_score: float = Field(ge=0.0, le=100.0, description="Overall compliance score")
    checks: List[PCI_DSSCheck] = Field(default_factory=list, description="List of PCI-DSS checks")
    card_data_protection_status: Dict[str, Any] = Field(default_factory=dict, description="Card data protection status")
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

