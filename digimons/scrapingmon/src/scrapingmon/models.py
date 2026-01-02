"""
Data models for scrapingmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for scrapingmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="scrapingmon", description="Digimon name")
    detection_methods: List[str] = Field(
        default_factory=lambda: ["rate_limit", "user_agent", "pattern", "behavior"],
        description="Detection methods enabled",
    )
    rate_limit_threshold: int = Field(default=100, ge=1, description="Requests per minute threshold")
    block_duration_minutes: int = Field(default=60, ge=1, description="Block duration in minutes")
    enable_captcha: bool = Field(default=False, description="Enable CAPTCHA challenges")
    suspicious_patterns: List[str] = Field(
        default_factory=lambda: ["bot", "crawler", "scraper", "spider"],
        description="Suspicious user agent patterns",
    )
    debug: bool = Field(default=False, description="Enable debug mode")


class ScrapingAttempt(BaseModel):
    """Scraping attempt information"""

    attempt_id: str = Field(description="Unique attempt identifier")
    ip_address: str = Field(description="IP address of the attempt")
    user_agent: str = Field(description="User agent string")
    request_count: int = Field(description="Number of requests")
    detection_method: str = Field(description="Method that detected scraping")
    severity: str = Field(description="Severity level (low/medium/high/critical)")
    timestamp: str = Field(description="Attempt timestamp")
    blocked: bool = Field(description="Whether the attempt was blocked")


class ScrapingAnalysis(BaseModel):
    """Result of scraping analysis"""

    total_requests: int = Field(description="Total requests analyzed")
    scraping_attempts: int = Field(description="Number of scraping attempts detected")
    blocked_attempts: int = Field(description="Number of attempts blocked")
    attempts_by_severity: Dict[str, int] = Field(default_factory=dict, description="Attempts by severity")
    attempts_by_method: Dict[str, int] = Field(default_factory=dict, description="Attempts by detection method")
    attempts: List[ScrapingAttempt] = Field(default_factory=list, description="List of scraping attempts")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Analysis statistics")


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
    detection_methods: str
    rate_limit_threshold: str
    version: str = "3.0.0"

