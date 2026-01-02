"""
Unit tests for Incidentmon (Mega)
"""

import pytest

from incidentmon.core import Incidentmon
from incidentmon.models import AnalysisResult, IncidentResponse


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Incidentmon"""
    return Incidentmon()


@pytest.fixture
def digimon_auto_contain():
    """Fixture con auto_contain habilitado"""
    return Incidentmon(config={"auto_contain": True, "severity_threshold": "high"})


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Incidentmon"
        assert digimon.mission == "The Gunslinger"
        assert digimon.role == "incident-response"

    def test_init_with_config(self, digimon_auto_contain):
        """Test inicialización con configuración"""
        assert digimon_auto_contain.auto_contain is True
        assert digimon_auto_contain.severity_threshold == "high"


class TestIncidentResponse:
    """Tests para respuesta a incidentes"""

    def test_respond_to_incident(self, digimon):
        """Test respuesta a incidente"""
        response = digimon.respond_to_incident("malware", "medium", "server-01")
        assert isinstance(response, IncidentResponse)
        assert response.incident_id
        assert response.severity == "medium"

    def test_respond_to_critical_incident(self, digimon_auto_contain):
        """Test respuesta a incidente crítico con auto_contain"""
        response = digimon_auto_contain.respond_to_incident("breach", "critical", "server-01")
        assert response.contained is True
        assert len(response.actions_taken) > 0


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_incident(self, digimon):
        """Test analyze con un incidente"""
        result = digimon.analyze(incident_type="malware", severity="medium", target="server-01")
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_multiple_incidents(self, digimon):
        """Test analyze con múltiples incidentes"""
        incidents = [
            {"incident_type": "malware", "severity": "high", "target": "server-01"},
            {"incident_type": "intrusion", "severity": "medium", "target": "server-02"},
        ]
        result = digimon.analyze(incidents=incidents)
        assert result.status == "success"
        assert result.data["total_incidents"] == 2

    def test_analyze_no_input(self, digimon):
        """Test analyze sin input"""
        result = digimon.analyze()
        assert result.status == "error"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"severity": "high", "target": "server-01"}
        assert digimon.validate(data) is True

    def test_validate_list(self, digimon):
        """Test validación con lista válida"""
        data = [{"severity": "high", "target": "server-01"}]
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Incidentmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
