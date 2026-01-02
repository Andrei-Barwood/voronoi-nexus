"""
Core functionality for Networkmon (Mega)

Networkmon monitorea tráfico de red en tiempo real con análisis avanzado.
Misión: A Kind and benevolent Despot
Rol: network-monitor
"""

import logging
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, NetworkConnection, TrafficAnalysis

logger = logging.getLogger(__name__)


class Networkmon:
    """
    Networkmon - Network Monitor (Mega)

    Descripción:
        Monitorea tráfico de red en tiempo real analizando conexiones,
        puertos, protocolos y detectando actividad sospechosa.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Networkmon.

        Args:
            config: Diccionario de configuración opcional:
                - max_connections: Máximo de conexiones (default: 1000)
                - alert_threshold: Umbral de alerta (default: 100/min)
                - track_ports: Rastrear puertos (default: True)
                - track_protocols: Rastrear protocolos (default: True)
        """
        self.name = "Networkmon"
        self.mission = "A Kind and benevolent Despot"
        self.role = "network-monitor"
        self.config = config or {}

        self.max_connections = int(self.config.get("max_connections", 1000))
        self.alert_threshold = int(self.config.get("alert_threshold", 100))
        self.track_ports = bool(self.config.get("track_ports", True))
        self.track_protocols = bool(self.config.get("track_protocols", True))

        # Almacenamiento interno de conexiones
        self.connections: List[NetworkConnection] = []

        logger.info(
            "Initialized %s - %s (max_conn=%d, threshold=%d/min)",
            self.name,
            self.role,
            self.max_connections,
            self.alert_threshold,
        )

    def add_connection(
        self,
        source_ip: str,
        dest_ip: str,
        source_port: Optional[int] = None,
        dest_port: Optional[int] = None,
        protocol: Optional[str] = None,
    ) -> None:
        """
        Añade una conexión al monitor.

        Args:
            source_ip: IP de origen
            dest_ip: IP de destino
            source_port: Puerto de origen (opcional)
            dest_port: Puerto de destino (opcional)
            protocol: Protocolo (opcional)
        """
        conn = NetworkConnection(
            source_ip=source_ip,
            dest_ip=dest_ip,
            source_port=source_port,
            dest_port=dest_port,
            protocol=protocol,
            timestamp=datetime.now().isoformat(),
        )
        self.connections.append(conn)

        # Limitar tamaño
        if len(self.connections) > self.max_connections:
            self.connections = self.connections[-self.max_connections :]

    def analyze_traffic(self) -> TrafficAnalysis:
        """
        Analiza el tráfico acumulado.

        Returns:
            TrafficAnalysis con resultados del análisis
        """
        unique_ips = set()
        port_usage: Dict[str, int] = defaultdict(int)
        protocol_usage: Dict[str, int] = defaultdict(int)
        suspicious: List[NetworkConnection] = []

        for conn in self.connections:
            unique_ips.add(conn.source_ip)
            unique_ips.add(conn.dest_ip)

            if self.track_ports and conn.dest_port:
                port_usage[str(conn.dest_port)] += 1

            if self.track_protocols and conn.protocol:
                protocol_usage[conn.protocol.upper()] += 1

            # Detectar conexiones sospechosas (puertos comunes de ataque)
            suspicious_ports = {22, 23, 3389, 1433, 3306, 5432}
            if conn.dest_port and conn.dest_port in suspicious_ports:
                suspicious.append(conn)

        # Análisis por minuto
        connections_per_minute = len(self.connections)
        alerts = []

        if connections_per_minute > self.alert_threshold:
            alerts.append(f"High connection rate: {connections_per_minute}/min")

        return TrafficAnalysis(
            total_connections=len(self.connections),
            unique_ips=sorted(list(unique_ips)),
            port_usage=dict(port_usage),
            protocol_usage=dict(protocol_usage),
            suspicious_connections=suspicious[:50],  # Limitar a 50
            analysis_summary={
                "total_connections": len(self.connections),
                "unique_ip_count": len(unique_ips),
                "connections_per_minute": connections_per_minute,
                "alerts": alerts,
                "most_used_port": max(port_usage.items(), key=lambda x: x[1])[0] if port_usage else None,
                "most_used_protocol": max(protocol_usage.items(), key=lambda x: x[1])[0] if protocol_usage else None,
            },
        )

    def analyze(self, connections: Optional[List[Dict[str, Any]]] = None) -> AnalysisResult:
        """
        Analiza tráfico: usa conexiones existentes o acepta nuevas.

        Args:
            connections: Lista opcional de conexiones a analizar

        Returns:
            AnalysisResult con resultados
        """
        if connections:
            # Limpiar y añadir nuevas conexiones
            self.connections.clear()
            for conn_data in connections:
                self.add_connection(
                    source_ip=conn_data.get("source_ip", ""),
                    dest_ip=conn_data.get("dest_ip", ""),
                    source_port=conn_data.get("source_port"),
                    dest_port=conn_data.get("dest_port"),
                    protocol=conn_data.get("protocol"),
                )

        analysis = self.analyze_traffic()
        status = "success" if analysis.total_connections > 0 else "warning"

        return AnalysisResult(
            status=status,
            message=f"Traffic analysis completed: {analysis.total_connections} connections",
            data=analysis.model_dump(),
        )

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada.
        """
        if data is None:
            return False
        if isinstance(data, list):
            return all(isinstance(item, dict) for item in data)
        return True

    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del Digimon.
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "max_connections": str(self.max_connections),
            "alert_threshold": str(self.alert_threshold),
        }

    def reset(self) -> None:
        """Resetea el estado del monitor."""
        self.connections.clear()
        logger.info("Networkmon state reset")


# Alias para retrocompatibilidad
Digimon = Networkmon
