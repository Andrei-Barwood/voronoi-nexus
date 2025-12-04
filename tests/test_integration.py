"""
Integration tests for SecurityPipeline
Verifica que Thirstmon y Bandidmon trabajen correctamente juntos
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from shared.pipeline import SecurityPipeline


@pytest.fixture
def pipeline():
    """Fixture para crear instancia del pipeline"""
    return SecurityPipeline()


class TestSecurityPipeline:
    """Tests de integración del pipeline completo"""
    
    def test_safe_traffic_flow(self, pipeline):
        """Test: Tráfico seguro pasa ambas fases"""
        urls = ["google.com", "github.com"]
        content = "Email: test@example.com"
        
        result = pipeline.process_traffic(urls, content)
        
        assert result['status'] == 'SAFE'
        assert result['phase_completed'] == 'data_protection'
        assert result['summary']['threats_found'] == 0
        assert result['summary']['data_redacted'] > 0
    
    def test_malicious_traffic_blocked(self, pipeline):
        """Test: Tráfico malicioso se bloquea en Fase 1"""
        urls = ["google.com", "evil-snake-oil.com"]
        content = "Este contenido no debería procesarse"
        
        result = pipeline.process_traffic(urls, content)
        
        assert result['status'] == 'BLOCKED'
        assert result['phase_completed'] == 'threat_filtering'
        assert result['summary']['threats_found'] > 0
        assert result['data_protection'] is None  # No llegó a Fase 2
    
    def test_empty_traffic(self, pipeline):
        """Test: Tráfico vacío"""
        result = pipeline.process_traffic([], "")
        
        assert result['status'] == 'SAFE'
        assert result['summary']['threats_found'] == 0
    
    def test_pipeline_info(self, pipeline):
        """Test: Información del pipeline"""
        info = pipeline.get_pipeline_info()
        
        assert 'pipeline_version' in info
        assert len(info['digimons_active']) == 2
        assert len(info['phases']) == 2
