"""
Core functionality for Thirstmon

This module contains the main logic and class definitions for Thirstmon.
Misión: Good, Honest Snake Oil
Rol: threat-filter
"""

import logging
from typing import Any, Dict, Optional, List

logger = logging.getLogger(__name__)


class Thirstmon:
    """
    Thirstmon - Cybersecurity Module
    
    Descripción:
        Filtra indicadores de compromiso maliciosos
    
    Attributes:
        name: Nombre del Digimon
        mission: Misión RDR2 inspiradora
        role: Rol en ciberseguridad
        threat_database: Lista interna de indicadores de compromiso (IoCs) conocidos
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Thirstmon
        
        Args:
            config: Diccionario de configuración opcional
        """
        self.name = "Thirstmon"
        self.mission = "Good, Honest Snake Oil"
        self.role = "threat-filter"
        self.config = config or {}
        
        # Base de datos simulada de amenazas (Snake Oil malicioso)
        # En versión Champion, esto vendría de una API externa o archivo CSV
        self.threat_database = {
            "evil-snake-oil.com",
            "192.168.66.6",
            "malware-download.net",
            "phishing-bank.com",
            "ransomware-host.io"
        }
        
        logger.info(f"Initialized {self.name} - {self.role}")
    
    def analyze(self, traffic_data: List[str]) -> Dict[str, Any]:
        """
        Ejecutar análisis principal filtrando tráfico contra la base de datos de amenazas.
        
        Args:
            traffic_data: Lista de URLs o IPs a analizar
            
        Returns:
            Diccionario con resultados del análisis (amenazas detectadas vs tráfico limpio)
        """
        logger.debug(f"Running analysis in {self.name} on {len(traffic_data)} items")
        
        detected_threats = []
        clean_traffic = []
        
        # Lógica de filtrado (El corazón de Thirstmon)
        for item in traffic_data:
            if item in self.threat_database:
                logger.warning(f"Threat detected: {item}")
                detected_threats.append(item)
            else:
                clean_traffic.append(item)
        
        # Construir reporte
        result = {
            "status": "success",
            "message": f"{self.name} analysis completed. Found {len(detected_threats)} threats.",
            "data": {
                "total_scanned": len(traffic_data),
                "threats_detected": detected_threats,
                "clean_traffic": clean_traffic,
                "threat_count": len(detected_threats)
            }
        }
        
        return result
    
    def validate(self, data: Any) -> bool:
        """
        Validar datos de entrada. Thirstmon espera una lista de strings.
        
        Args:
            data: Datos a validar
        
        Returns:
            True si es una lista válida, False en caso contrario
        """
        if not isinstance(data, list):
            logger.error("Input data must be a list")
            return False
        
        if not all(isinstance(item, str) for item in data):
            logger.error("All items in the list must be strings")
            return False
            
        return True
    
    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del Digimon
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Rookie",
            "database_size": str(len(self.threat_database))
        }


# Alias para retrocompatibilidad
Digimon = Thirstmon
