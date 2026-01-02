"""
Data models for fuzzymon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for fuzzymon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="fuzzymon", description="Digimon name")
    max_iterations: int = Field(default=1000, ge=1, description="Maximum fuzzing iterations")
    mutation_rate: float = Field(default=0.1, ge=0.0, le=1.0, description="Mutation rate")
    timeout_seconds: int = Field(default=5, ge=1, description="Timeout per test in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


class FuzzResult(BaseModel):
    """Result of fuzzing operation"""

    total_tests: int = Field(description="Total tests performed")
    crashes_found: int = Field(default=0, description="Number of crashes detected")
    hangs_found: int = Field(default=0, description="Number of hangs detected")
    bugs_found: List[str] = Field(default_factory=list, description="List of bugs found")
    coverage_percent: float = Field(default=0.0, description="Code coverage percentage")
    fuzz_summary: Dict[str, Any] = Field(default_factory=dict, description="Fuzzing summary")


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
    max_iterations: str
    mutation_rate: str
    version: str = "3.0.0"
