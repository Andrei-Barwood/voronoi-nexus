"""
Unit tests for Biometricmon (Mega)
"""

import pytest

from biometricmon.core import Biometricmon
from biometricmon.models import AnalysisResult, BiometricAnalysis, BiometricData


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Biometricmon"""
    return Biometricmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Biometricmon"
        assert digimon.mission == "My Last Boy"
        assert digimon.role == "biometric-handler"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"min_confidence": 0.90, "enable_liveness": False}
        digimon = Biometricmon(config=config)
        assert digimon.min_confidence == 0.90
        assert digimon.enable_liveness is False


class TestBiometricOperations:
    """Tests para operaciones biométricas"""

    def test_register_biometric(self, digimon):
        """Test registrar template biométrico"""
        bio = digimon.register_biometric("user1", "fingerprint", "template_data", 0.98, True)
        assert isinstance(bio, BiometricData)
        assert bio.user_id == "user1"

    def test_analyze_biometrics(self, digimon):
        """Test análisis de templates"""
        digimon.register_biometric("user1", "fingerprint", "template1", 0.98)
        analysis = digimon.analyze_biometrics()
        assert isinstance(analysis, BiometricAnalysis)
        assert analysis.total_templates == 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_biometrics(self, digimon):
        """Test analyze con analyze action"""
        result = digimon.analyze(action="analyze")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_register(self, digimon):
        """Test analyze con register action"""
        bio_data = {
            "user_id": "user1",
            "biometric_type": "fingerprint",
            "template_data": "template123",
            "confidence": 0.98,
            "liveness_verified": True,
        }
        result = digimon.analyze(action="register", biometric_data=bio_data)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_dict(self, digimon):
        """Test validación con diccionario válido"""
        data = {"user_id": "user1", "biometric_type": "fingerprint"}
        assert digimon.validate(data) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Biometricmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

