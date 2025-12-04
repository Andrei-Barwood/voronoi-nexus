"""
Security Pipeline - Integrates multiple Digimons

Este módulo orquesta el trabajo conjunto de Thirstmon y Bandidmon
para crear un pipeline de seguridad completo.
"""

import logging
from typing import Dict, Any, List
import sys
import os

# Agregar rutas de los Digimons al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../digimons/thirstmon/src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../digimons/bandidmon/src'))

from thirstmon.core import Thirstmon
from bandidmon.core import Bandidmon

logger = logging.getLogger(__name__)


class SecurityPipeline:
    """
    Pipeline de seguridad que integra múltiples Digimons.
    
    Flujo:
    1. Thirstmon filtra amenazas en URLs/IPs
    2. Si el tráfico es limpio, Bandidmon protege datos sensibles
    3. Retorna un reporte consolidado
    """
    
    def __init__(self):
        """Inicializar el pipeline con los Digimons necesarios"""
        self.threat_filter = Thirstmon()
        self.data_protector = Bandidmon()
        
        logger.info("Security Pipeline initialized with Thirstmon + Bandidmon")
    
    def process_traffic(self, urls: List[str], content: str) -> Dict[str, Any]:
        """
        Procesa tráfico web completo: URLs + contenido
        
        Args:
            urls: Lista de URLs/IPs a verificar
            content: Contenido del tráfico (texto, emails, etc)
            
        Returns:
            Reporte consolidado con resultados de ambas fases
        """
        logger.info(f"Processing {len(urls)} URLs and {len(content)} chars of content")
        
        # ===== FASE 1: FILTRADO DE AMENAZAS (Thirstmon) =====
        threat_analysis = self.threat_filter.analyze(urls)
        
        # Si se detectaron amenazas, bloquear todo
        if threat_analysis['data']['threat_count'] > 0:
            logger.warning(f"Threats detected! Blocking traffic.")
            return {
                "status": "BLOCKED",
                "phase_completed": "threat_filtering",
                "threat_analysis": threat_analysis,
                "data_protection": None,
                "summary": {
                    "threats_found": threat_analysis['data']['threat_count'],
                    "blocked_urls": threat_analysis['data']['threats_detected'],
                    "action": "Traffic blocked by Thirstmon"
                }
            }
        
        # ===== FASE 2: PROTECCIÓN DE DATOS (Bandidmon) =====
        logger.info("No threats found. Proceeding to data protection...")
        data_analysis = self.data_protector.analyze(content)
        
        return {
            "status": "SAFE",
            "phase_completed": "data_protection",
            "threat_analysis": threat_analysis,
            "data_protection": data_analysis,
            "summary": {
                "threats_found": 0,
                "urls_scanned": len(urls),
                "data_redacted": data_analysis['data']['redacted_count'],
                "action": "Content processed and sanitized",
                "safe_content": data_analysis['data']['safe_text']
            }
        }
    
    def get_pipeline_info(self) -> Dict[str, Any]:
        """Información sobre los Digimons en el pipeline"""
        return {
            "pipeline_version": "0.1.0",
            "digimons_active": [
                self.threat_filter.get_info(),
                self.data_protector.get_info()
            ],
            "phases": [
                "1. Threat Filtering (Thirstmon)",
                "2. Data Protection (Bandidmon)"
            ]
        }
