"""
Data models for permissionmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for permissionmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="permissionmon", description="Digimon name")
    check_file_permissions: bool = Field(default=True, description="Check file permissions")
    check_directory_permissions: bool = Field(default=True, description="Check directory permissions")
    enforce_least_privilege: bool = Field(default=True, description="Enforce least privilege principle")
    debug: bool = Field(default=False, description="Enable debug mode")


class PermissionCheck(BaseModel):
    """Result of permission check"""

    resource: str = Field(description="Resource being checked")
    resource_type: str = Field(description="Type of resource (file/directory/endpoint)")
    required_permission: str = Field(description="Required permission (read/write/execute)")
    granted: bool = Field(description="Whether permission is granted")
    current_permissions: Optional[str] = Field(default=None, description="Current permissions (octal)")
    violations: List[str] = Field(default_factory=list, description="Permission violations")


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
    enforce_least_privilege: str
    version: str = "3.0.0"

