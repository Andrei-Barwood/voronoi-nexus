"""
Data models for vulnemon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for vulnemon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="vulnemon", description="Digimon name")
    severity_threshold: str = Field(default="medium", description="Minimum severity to report")
    check_cves: bool = Field(default=True, description="Check against CVE database")
    scan_depth: int = Field(default=5, ge=1, le=10, description="Scan depth level")
    debug: bool = Field(default=False, description="Enable debug mode")


class Vulnerability(BaseModel):
    """Vulnerability information"""

    cve_id: Optional[str] = Field(default=None, description="CVE identifier")
    severity: str = Field(description="Severity level (critical/high/medium/low)")
    description: str = Field(description="Vulnerability description")
    affected_component: str = Field(description="Affected component/version")
    recommendation: Optional[str] = Field(default=None, description="Remediation recommendation")


class ScanResult(BaseModel):
    """Result of vulnerability scan"""

    total_vulnerabilities: int = Field(description="Total vulnerabilities found")
    critical_count: int = Field(default=0, description="Critical severity count")
    high_count: int = Field(default=0, description="High severity count")
    medium_count: int = Field(default=0, description="Medium severity count")
    low_count: int = Field(default=0, description="Low severity count")
    vulnerabilities: List[Vulnerability] = Field(default_factory=list, description="List of vulnerabilities")
    scan_summary: Dict[str, Any] = Field(default_factory=dict, description="Scan summary")


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
    severity_threshold: str
    scan_depth: str
    version: str = "3.0.0"
