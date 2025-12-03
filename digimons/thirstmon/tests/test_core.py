"""
Unit tests for thirstmon core module
"""

import pytest
from thirstmon.core import Uthirstmon


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Uthirstmon"""
    return Uthirstmon()


class TestInitialization:
    """Tests para inicialización"""
    
    def test_init_default(self):
        """Test inicialización con valores por defecto"""
        digimon = Uthirstmon()
        assert digimon.name == "thirstmon"
        assert digimon.mission == "Good, Honest Snake Oil"
        assert digimon.role == "threat-filter"
    
    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"debug": True}
        digimon = Uthirstmon(config=config)
        assert digimon.config == config


class TestAnalysis:
    """Tests para funcionalidad de análisis"""
    
    def test_analyze_returns_dict(self, digimon):
        """Test que analyze() retorna diccionario"""
        result = digimon.analyze()
        assert isinstance(result, dict)
        assert "status" in result
        assert "message" in result
    
    def test_analyze_success_status(self, digimon):
        """Test que analyze() retorna status success"""
        result = digimon.analyze()
        assert result["status"] == "success"


class TestValidation:
    """Tests para validación"""
    
    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False
    
    def test_validate_valid_data(self, digimon):
        """Test validación con datos válidos"""
        assert digimon.validate({"key": "value"}) is True


class TestInfo:
    """Tests para información del Digimon"""
    
    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "thirstmon"
        assert info["status"] == "Rookie"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
