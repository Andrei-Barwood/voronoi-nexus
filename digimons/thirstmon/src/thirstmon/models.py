"""
Data models for thirstmon

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class DigimonConfig(BaseModel):
    """Configuration model for thirstmon"""
    
    name: str = Field(default="thirstmon", description="Digimon name")
    debug: bool = Field(default=False, description="Enable debug mode")
    timeout: int = Field(default=30, ge=1, description="Request timeout in seconds")
    
    class Config:
        """Pydantic config"""
        frozen = True


class AnalysisResult(BaseModel):
    """Result model for analysis operations"""
    
    status: str = Field(description="Status of the analysis")
    message: str = Field(description="Descriptive message")
    data: Dict[str, Any] = Field(default_factory=dict, description="Result data")
    errors: Optional[list] = Field(default=None, description="List of errors if any")


class DigimonInfo(BaseModel):
    """Information model for Digimon metadata"""
    
    name: str
    mission: str
    role: str
    status: str
    version: str = "0.1.0"
