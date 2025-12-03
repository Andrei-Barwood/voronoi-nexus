"""
Unit tests for Thirstmon core module
"""

import pytest
from thirstmon.core import Thirstmon


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Thirstmon"""
    return Thirstmon()


class TestInitialization:
    """Tests para inicialización"""
    
    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Thirstmon"
        assert digimon.mission == "Good, Honest Snake Oil"
        assert isinstance(digimon.threat_database, set)
        assert "evil-snake-oil.com" in digimon.threat_database


class TestAnalysis:
    """Tests para funcionalidad de análisis"""
    
    def test_analyze_detection(self, digimon):
        """Test que verifica si detecta amenazas correctamente"""
        # Datos de prueba: 2 amenazas conocidas y 1 sitio seguro
        input_data = [
            "google.com",           # Seguro
            "evil-snake-oil.com",   # Amenaza
            "malware-download.net"  # Amenaza
        ]
        
        result = digimon.analyze(input_data)
        
        assert result["status"] == "success"
        assert result["data"]["total_scanned"] == 3
        assert result["data"]["threat_count"] == 2
        
        # Verificar que clasificó bien
        assert "evil-snake-oil.com" in result["data"]["threats_detected"]
        assert "google.com" in result["data"]["clean_traffic"]

    def test_analyze_empty_list(self, digimon):
        """Test con lista vacía"""
        result = digimon.analyze([])
        assert result["data"]["total_scanned"] == 0
        assert result["data"]["threat_count"] == 0


class TestValidation:
    """Tests para validación"""
    
    def test_validate_invalid_type(self, digimon):
        """Test debe fallar si no es una lista"""
        assert digimon.validate("no soy una lista") is False
        assert digimon.validate(123) is False
    
    def test_validate_invalid_content(self, digimon):
        """Test debe fallar si la lista contiene cosas que no son strings"""
        assert digimon.validate(["google.com", 123]) is False
    
    def test_validate_valid_data(self, digimon):
        """Test validación con datos válidos"""
        assert digimon.validate(["google.com", "yahoo.com"]) is True


class TestInfo:
    """Tests para información del Digimon"""
    
    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario con info extra"""
        info = digimon.get_info()
        assert info["name"] == "Thirstmon"
        assert "database_size" in info
