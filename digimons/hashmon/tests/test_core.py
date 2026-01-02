"""
Unit tests for Hashmon (Mega)
"""

import pytest

from hashmon.core import Hashmon
from hashmon.models import AnalysisResult, HashResult, VerificationResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Hashmon"""
    return Hashmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Hashmon"
        assert digimon.mission == "Forever Yours, Arthur"
        assert digimon.role == "hash-validator"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"default_algorithm": "sha512", "enable_hmac": False}
        digimon = Hashmon(config=config)
        assert digimon.default_algorithm == "sha512"
        assert digimon.enable_hmac is False


class TestHashComputation:
    """Tests para cálculo de hash"""

    def test_compute_hash(self, digimon):
        """Test cálculo de hash"""
        data = b"test data"
        result = digimon.compute_hash(data)
        assert isinstance(result, HashResult)
        assert result.algorithm == digimon.default_algorithm
        assert len(result.hash_value) > 0

    def test_compute_hash_different_algorithm(self, digimon):
        """Test cálculo con algoritmo diferente"""
        data = b"test data"
        result = digimon.compute_hash(data, algorithm="sha512")
        assert result.algorithm == "sha512"


class TestHashVerification:
    """Tests para verificación de hash"""

    def test_verify_hash_match(self, digimon):
        """Test verificación con hash que coincide"""
        data = b"test data"
        hash_result = digimon.compute_hash(data)
        verify_result = digimon.verify_hash(data, hash_result.hash_value)
        assert verify_result.verified is True
        assert verify_result.match is True

    def test_verify_hash_mismatch(self, digimon):
        """Test verificación con hash que no coincide"""
        data = b"test data"
        verify_result = digimon.verify_hash(data, "invalid_hash")
        assert verify_result.verified is False
        assert verify_result.match is False


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_compute(self, digimon):
        """Test analyze para cálculo"""
        data = b"test data"
        result = digimon.analyze(data=data)
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_verify(self, digimon):
        """Test analyze para verificación"""
        data = b"test data"
        hash_result = digimon.compute_hash(data)
        result = digimon.analyze(data=data, expected_hash=hash_result.hash_value)
        assert result.status == "success"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_bytes(self, digimon):
        """Test validación con bytes"""
        assert digimon.validate(b"test") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Hashmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

