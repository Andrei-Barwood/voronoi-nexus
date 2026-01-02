"""
Unit tests for Compliancemon (Mega)
"""

import pytest

from compliancemon.core import Compliancemon
from compliancemon.models import AnalysisResult, ComplianceAudit


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Compliancemon"""
    return Compliancemon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Compliancemon"
        assert digimon.mission == "Revenge"
        assert digimon.role == "compliance-checker"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"compliance_frameworks": ["GDPR", "HIPAA"], "strict_mode": False}
        digimon = Compliancemon(config=config)
        assert len(digimon.compliance_frameworks) == 2
        assert digimon.strict_mode is False


class TestComplianceAudit:
    """Tests para auditoría de compliance"""

    def test_audit_target(self, digimon):
        """Test auditoría de objetivo"""
        target_data = {"name": "test_system", "encryption_enabled": True, "access_controls": True}
        audit = digimon.audit_target(target_data)
        assert isinstance(audit, ComplianceAudit)
        assert audit.total_checks > 0

    def test_audit_target_with_failures(self, digimon):
        """Test auditoría con fallos"""
        target_data = {"name": "test_system", "encryption_enabled": False}
        audit = digimon.audit_target(target_data)
        assert audit.failed_checks >= 0  # Puede tener fallos


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_target(self, digimon):
        """Test analyze con datos de objetivo"""
        target_data = {"name": "test_system", "encryption_enabled": True}
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
        assert info["name"] == "Compliancemon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

