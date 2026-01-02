"""
Data models for networkmon (Mega).

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class DigimonConfig(BaseModel):
    """Configuration model for networkmon"""

    model_config = ConfigDict(frozen=True)

    name: str = Field(default="networkmon", description="Digimon name")
    max_connections: int = Field(default=1000, ge=1, description="Maximum connections to monitor")
    alert_threshold: int = Field(default=100, ge=1, description="Alert threshold for connections per minute")
    track_ports: bool = Field(default=True, description="Track port usage")
    track_protocols: bool = Field(default=True, description="Track protocol usage")
    debug: bool = Field(default=False, description="Enable debug mode")


class NetworkConnection(BaseModel):
    """Network connection information"""

    source_ip: str = Field(description="Source IP address")
    dest_ip: str = Field(description="Destination IP address")
    source_port: Optional[int] = Field(default=None, description="Source port")
    dest_port: Optional[int] = Field(default=None, description="Destination port")
    protocol: Optional[str] = Field(default=None, description="Protocol (TCP/UDP/etc)")
    timestamp: str = Field(description="Connection timestamp")


class TrafficAnalysis(BaseModel):
    """Result of traffic analysis"""

    total_connections: int = Field(description="Total connections analyzed")
    unique_ips: List[str] = Field(default_factory=list, description="Unique IP addresses")
    port_usage: Dict[str, int] = Field(default_factory=dict, description="Port usage statistics")
    protocol_usage: Dict[str, int] = Field(default_factory=dict, description="Protocol usage statistics")
    suspicious_connections: List[NetworkConnection] = Field(
        default_factory=list, description="Suspicious connections detected"
    )
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
    max_connections: str
    alert_threshold: str
    version: str = "3.0.0"
