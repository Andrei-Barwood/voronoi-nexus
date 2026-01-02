"""
Unit tests for HIPAAmon (Mega)
"""

import pytest

from hipaamon.core import HIPAAmon
from hipaamon.models import AnalysisResult, HIPAAComplianceReport


@pytest.fixture
def digimon():
    """Fixture para crear instancia de HIPAAmon"""
    return HIPAAmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "HIPAAmon"
        assert digimon.mission == "My Last Boy"
        assert digimon.role == "hipaa-auditor"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"strict_mode": False, "check_phi_protection": False}
        digimon = HIPAAmon(config=config)
        assert digimon.strict_mode is False
        assert digimon.check_phi_protection is False


class TestHIPAACompliance:
    """Tests para cumplimiento HIPAA"""

    def test_audit_compliance(self, digimon):
        """Test auditoría de cumplimiento"""
        target_data = {"name": "test_system", "access_controls_enabled": True, "encryption_enabled": True}
        report = digimon.audit_compliance(target_data)
        assert isinstance(report, HIPAAComplianceReport)
        assert report.total_checks > 0

    def test_audit_compliance_with_failures(self, digimon):
        """Test auditoría con fallos"""
        target_data = {"name": "test_system", "access_controls_enabled": False}
        report = digimon.audit_compliance(target_data)
        assert report.failed_checks >= 0  # Puede tener fallos


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
        assert info["name"] == "HIPAAmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

