"""
Unit tests for Authmon (Mega)
"""

import pytest

from authmon.core import Authmon
from authmon.models import AnalysisResult, AuthResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Authmon"""
    return Authmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Authmon"
        assert digimon.mission == "The Noblest of Men"
        assert digimon.role == "auth-handler"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"max_attempts": 3, "lockout_duration": 600}
        digimon = Authmon(config=config)
        assert digimon.max_attempts == 3
        assert digimon.lockout_duration == 600


class TestAuthentication:
    """Tests para autenticación"""

    def test_authenticate_success(self, digimon):
        """Test autenticación exitosa"""
        result = digimon.authenticate("user1", {"password": "validpass"}, "password")
        assert isinstance(result, AuthResult)
        assert result.success is True

    def test_authenticate_failure(self, digimon):
        """Test autenticación fallida"""
        result = digimon.authenticate("user1", {"password": ""}, "password")
        assert result.success is False


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_success(self, digimon):
        """Test analyze con autenticación exitosa"""
        result = digimon.analyze("user1", {"password": "validpass"})
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_failure(self, digimon):
        """Test analyze con autenticación fallida"""
        result = digimon.analyze("user1", {"password": ""})
        assert result.status in ["error", "warning"]


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"user_id": "user1", "credentials": {"password": "pass"}}
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Authmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

