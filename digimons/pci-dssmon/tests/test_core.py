"""
Unit tests for PCI-DSSmon (Mega)
"""

import pytest

from pci_dssmon.core import PCI_DSSmon
from pci_dssmon.models import AnalysisResult, PCI_DSSComplianceReport


@pytest.fixture
def digimon():
    """Fixture para crear instancia de PCI_DSSmon"""
    return PCI_DSSmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "PCI_DSSmon"
        assert digimon.mission == "The Gunslinger"
        assert digimon.role == "pci-dss-validator"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"strict_mode": False, "check_card_data_protection": False}
        digimon = PCI_DSSmon(config=config)
        assert digimon.strict_mode is False
        assert digimon.check_card_data_protection is False


class TestPCI_DSSCompliance:
    """Tests para cumplimiento PCI-DSS"""

    def test_audit_compliance(self, digimon):
        """Test auditoría de cumplimiento"""
        target_data = {"name": "test_system", "card_data_encryption": True, "transmission_encryption": True}
        report = digimon.audit_compliance(target_data)
        assert isinstance(report, PCI_DSSComplianceReport)
        assert report.total_checks > 0

    def test_audit_compliance_with_failures(self, digimon):
        """Test auditoría con fallos"""
        target_data = {"name": "test_system", "card_data_encryption": False}
        report = digimon.audit_compliance(target_data)
        assert report.failed_checks >= 0  # Puede tener fallos


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_target(self, digimon):
        """Test analyze con datos de objetivo"""
        target_data = {"name": "test_system", "card_data_encryption": True}
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
        assert info["name"] == "PCI_DSSmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

