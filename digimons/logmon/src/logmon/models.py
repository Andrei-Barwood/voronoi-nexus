"""
Data models for logmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for logmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="logmon", description="Digimon name")
    log_levels: List[str] = Field(
        default_factory=lambda: ["ERROR", "WARN", "INFO", "DEBUG"],
        description="Log levels to process",
    )
    pattern_detection: bool = Field(default=True, description="Enable pattern detection")
    correlation_window: int = Field(default=300, ge=1, description="Correlation window in seconds")
    debug: bool = Field(default=False, description="Enable debug mode")


class LogEntry(BaseModel):
    """Log entry information"""

    timestamp: str = Field(description="Log timestamp")
    level: str = Field(description="Log level")
    message: str = Field(description="Log message")
    source: Optional[str] = Field(default=None, description="Log source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class LogAnalysis(BaseModel):
    """Result of log analysis"""

    total_entries: int = Field(description="Total log entries analyzed")
    entries_by_level: Dict[str, int] = Field(default_factory=dict, description="Entries grouped by level")
    patterns_detected: List[str] = Field(default_factory=list, description="Patterns detected")
    errors_found: List[LogEntry] = Field(default_factory=list, description="Error entries")
    warnings_found: List[LogEntry] = Field(default_factory=list, description="Warning entries")
    analysis_summary: Dict[str, Any] = Field(default_factory=dict, description="Summary statistics")


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
    log_levels: str
    correlation_window: str
    version: str = "3.0.0"
