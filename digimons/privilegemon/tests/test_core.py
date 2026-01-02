"""
Unit tests for Privilegemon (Mega)
"""

import pytest

from privilegemon.core import Privilegemon
from privilegemon.models import AnalysisResult, PrivilegeAudit, PrivilegeEvent


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Privilegemon"""
    return Privilegemon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Privilegemon"
        assert digimon.mission == "Clemens Point"
        assert digimon.role == "privilege-auditor"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"require_justification": False, "max_elevation_duration": 1800}
        digimon = Privilegemon(config=config)
        assert digimon.require_justification is False
        assert digimon.max_elevation_duration == 1800


class TestPrivilegeOperations:
    """Tests para operaciones de privilegios"""

    def test_request_elevation(self, digimon):
        """Test solicitar elevación"""
        event = digimon.request_elevation("user1", "admin", "Maintenance task")
        assert isinstance(event, PrivilegeEvent)
        assert event.user_id == "user1"

    def test_audit_privileges(self, digimon):
        """Test auditoría de privilegios"""
        digimon.request_elevation("user1", "admin", "Task")
        audit = digimon.audit_privileges()
        assert isinstance(audit, PrivilegeAudit)
        assert audit.total_events >= 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_audit(self, digimon):
        """Test analyze con audit action"""
        result = digimon.analyze(action="audit")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_request(self, digimon):
        """Test analyze con request action"""
        elevation_data = {"user_id": "user1", "privilege": "admin", "justification": "Task"}
        result = digimon.analyze(action="request", elevation_data=elevation_data)
        assert result.status in ["success", "warning"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"user_id": "user1", "privilege": "admin"}
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Privilegemon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

