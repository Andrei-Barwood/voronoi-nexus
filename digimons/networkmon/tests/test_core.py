"""
Unit tests for Networkmon (Mega)
"""

import pytest

from networkmon.core import Networkmon
from networkmon.models import AnalysisResult, TrafficAnalysis


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Networkmon"""
    return Networkmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Networkmon"
        assert digimon.mission == "A Kind and benevolent Despot"
        assert digimon.role == "network-monitor"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"max_connections": 500, "alert_threshold": 50}
        digimon = Networkmon(config=config)
        assert digimon.max_connections == 500
        assert digimon.alert_threshold == 50


class TestConnectionTracking:
    """Tests para rastreo de conexiones"""

    def test_add_connection(self, digimon):
        """Test añadir conexión"""
        digimon.add_connection("192.168.1.1", "10.0.0.1", source_port=12345, dest_port=80, protocol="TCP")
        assert len(digimon.connections) == 1
        assert digimon.connections[0].source_ip == "192.168.1.1"

    def test_analyze_traffic(self, digimon):
        """Test análisis de tráfico"""
        digimon.add_connection("192.168.1.1", "10.0.0.1", dest_port=80, protocol="TCP")
        digimon.add_connection("192.168.1.2", "10.0.0.2", dest_port=443, protocol="TCP")
        analysis = digimon.analyze_traffic()
        assert isinstance(analysis, TrafficAnalysis)
        assert analysis.total_connections == 2
        assert len(analysis.unique_ips) == 4


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_with_connections(self, digimon):
        """Test analyze con lista de conexiones"""
        connections = [
            {"source_ip": "192.168.1.1", "dest_ip": "10.0.0.1", "dest_port": 80, "protocol": "TCP"}
        ]
        result = digimon.analyze(connections=connections)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_without_connections(self, digimon):
        """Test analyze sin conexiones previas"""
        result = digimon.analyze()
        assert isinstance(result, AnalysisResult)
        assert result.status == "warning"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_list(self, digimon):
        """Test validación con lista"""
        assert digimon.validate([{"source_ip": "1.1.1.1", "dest_ip": "2.2.2.2"}]) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Networkmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
