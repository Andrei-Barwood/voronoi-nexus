"""
Unit tests for Encryptionmon (Mega)
"""

import pytest

from encryptionmon.core import Encryptionmon
from encryptionmon.models import AnalysisResult, EncryptionKey


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Encryptionmon"""
    return Encryptionmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Encryptionmon"
        assert digimon.mission == "Forced Proximity"
        assert digimon.role == "encryption-manager"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"default_algorithm": "ChaCha20-Poly1305", "key_rotation_days": 60}
        digimon = Encryptionmon(config=config)
        assert digimon.default_algorithm == "ChaCha20-Poly1305"
        assert digimon.key_rotation_days == 60


class TestKeyManagement:
    """Tests para gestión de claves"""

    def test_generate_key(self, digimon):
        """Test generación de clave"""
        key = digimon.generate_key()
        assert isinstance(key, EncryptionKey)
        assert key.key_id is not None
        assert key.algorithm == digimon.default_algorithm

    def test_rotate_key(self, digimon):
        """Test rotación de clave"""
        key = digimon.generate_key()
        result = digimon.rotate_key(key.key_id)
        assert result.success is True
        assert result.keys_rotated == 1

    def test_revoke_key(self, digimon):
        """Test revocación de clave"""
        key = digimon.generate_key()
        result = digimon.revoke_key(key.key_id)
        assert result.success is True
        assert result.keys_revoked == 1


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_generate(self, digimon):
        """Test analyze con operación generate"""
        result = digimon.analyze(operation="generate")
        assert isinstance(result, AnalysisResult)
        assert result.status == "success"

    def test_analyze_list(self, digimon):
        """Test analyze con operación list"""
        digimon.generate_key()
        result = digimon.analyze(operation="list")
        assert result.status == "success"
        assert result.data["total_keys"] >= 1


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_operation(self, digimon):
        """Test validación con operación válida"""
        assert digimon.validate("generate") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Encryptionmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

