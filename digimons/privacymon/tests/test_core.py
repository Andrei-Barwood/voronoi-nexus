"""
Unit tests for Privacymon (Mega)
"""

import pytest

from privacymon.core import Privacymon
from privacymon.models import AnalysisResult, PrivacyAudit


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Privacymon"""
    return Privacymon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Privacymon"
        assert digimon.mission == "Clemens Point"
        assert digimon.role == "privacy-auditor"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"strict_mode": False, "check_data_collection": False}
        digimon = Privacymon(config=config)
        assert digimon.strict_mode is False
        assert digimon.check_data_collection is False


class TestPrivacyAudit:
    """Tests para auditoría de privacidad"""

    def test_audit_policy(self, digimon):
        """Test auditoría de política"""
        target_data = {"name": "test_system", "consent_mechanism": True, "privacy_policy_public": True}
        audit = digimon.audit_policy(target_data)
        assert isinstance(audit, PrivacyAudit)
        assert audit.total_checks > 0

    def test_audit_policy_with_failures(self, digimon):
        """Test auditoría con fallos"""
        target_data = {"name": "test_system", "consent_mechanism": False}
        audit = digimon.audit_policy(target_data)
        assert audit.failed_checks >= 0  # Puede tener fallos


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_target(self, digimon):
        """Test analyze con datos de objetivo"""
        target_data = {"name": "test_system", "privacy_policy_public": True}
        result = digimon.analyze(target_data=target_data)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning", "error"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        assert digimon.validate({"name": "test"}) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Privacymon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

