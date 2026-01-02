"""
Unit tests for Policymon (Mega)
"""

import pytest

from policymon.core import Policymon
from policymon.models import AnalysisResult, PolicyCheck


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Policymon"""
    return Policymon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Policymon"
        assert digimon.mission == "Charlotte Balfour"
        assert digimon.role == "policy-enforcer"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"strict_mode": False, "check_permissions": False}
        digimon = Policymon(config=config)
        assert digimon.strict_mode is False
        assert digimon.check_permissions is False


class TestPolicyChecking:
    """Tests para verificación de políticas"""

    def test_check_password_policy_compliant(self, digimon):
        """Test verificación de política de contraseña cumplida"""
        data = {"password": "SecurePass123!"}
        result = digimon.check_policy("password_policy", data)
        assert isinstance(result, PolicyCheck)
        assert result.compliant is True

    def test_check_password_policy_violations(self, digimon):
        """Test verificación de política de contraseña con violaciones"""
        data = {"password": "weak"}
        result = digimon.check_policy("password_policy", data)
        assert result.compliant is False
        assert len(result.violations) > 0

    def test_check_encryption_policy(self, digimon):
        """Test verificación de política de encriptación"""
        data = {"key_bits": 256, "is_aead": True}
        result = digimon.check_policy("encryption_policy", data)
        assert isinstance(result, PolicyCheck)


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_policy(self, digimon):
        """Test analyze con una política"""
        policy_check = {"policy_name": "password_policy", "data": {"password": "SecurePass123!"}}
        result = digimon.analyze(policy_check=policy_check)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_multiple_policies(self, digimon):
        """Test analyze con múltiples políticas"""
        policy_checks = [
            {"policy_name": "password_policy", "data": {"password": "SecurePass123!"}},
            {"policy_name": "encryption_policy", "data": {"key_bits": 256, "is_aead": True}},
        ]
        result = digimon.analyze(policy_checks=policy_checks)
        assert result.status == "success"
        assert result.data["total_checks"] == 2

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
        data = {"policy_name": "test", "data": {}}
        assert digimon.validate(data) is True

    def test_validate_list(self, digimon):
        """Test validación con lista válida"""
        data = [{"policy_name": "test", "data": {}}]
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Policymon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
