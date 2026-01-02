"""
Data models for biometricmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for biometricmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="biometricmon", description="Digimon name")
    supported_types: List[str] = Field(
        default_factory=lambda: ["fingerprint", "face", "iris", "voice"],
        description="Supported biometric types",
    )
    min_confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Minimum confidence threshold")
    enable_liveness: bool = Field(default=True, description="Enable liveness detection")
    debug: bool = Field(default=False, description="Enable debug mode")


class BiometricData(BaseModel):
    """Biometric data information"""

    biometric_id: str = Field(description="Unique biometric identifier")
    user_id: str = Field(description="User ID")
    biometric_type: str = Field(description="Type of biometric (fingerprint/face/iris/voice)")
    template_hash: str = Field(description="Hash of biometric template")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score")
    liveness_verified: bool = Field(default=False, description="Whether liveness was verified")
    created_at: str = Field(description="Creation timestamp")


class BiometricAnalysis(BaseModel):
    """Result of biometric analysis"""

    total_templates: int = Field(description="Total biometric templates")
    templates_by_type: Dict[str, int] = Field(default_factory=dict, description="Templates by type")
    low_confidence: int = Field(default=0, description="Number of low confidence templates")
    liveness_verified: int = Field(default=0, description="Number with liveness verification")
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
    supported_types: str
    min_confidence: str
    version: str = "3.0.0"

