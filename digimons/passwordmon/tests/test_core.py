"""
Unit tests for Passwordmon (Mega)
"""

import pytest

from passwordmon.core import Passwordmon
from passwordmon.models import AnalysisResult, PasswordValidation


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Passwordmon"""
    return Passwordmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Passwordmon"
        assert digimon.mission == "The Gilded Cage"
        assert digimon.role == "password-validator"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"min_length": 16, "require_special": False}
        digimon = Passwordmon(config=config)
        assert digimon.min_length == 16
        assert digimon.require_special is False


class TestPasswordValidation:
    """Tests para validación de contraseñas"""

    def test_validate_password_strong(self, digimon):
        """Test validación de contraseña fuerte"""
        result = digimon.validate_password("SecurePass123!@#")
        assert isinstance(result, PasswordValidation)
        assert result.strength in ["strong", "medium"]

    def test_validate_password_weak(self, digimon):
        """Test validación de contraseña débil"""
        result = digimon.validate_password("weak")
        assert result.valid is False
        assert len(result.violations) > 0


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_single_password(self, digimon):
        """Test analyze con una contraseña"""
        result = digimon.analyze(password="SecurePass123!")
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_multiple_passwords(self, digimon):
        """Test analyze con múltiples contraseñas"""
        passwords = ["SecurePass123!", "weak"]
        result = digimon.analyze(passwords=passwords)
        assert result.status in ["success", "warning"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("password123") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Passwordmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

