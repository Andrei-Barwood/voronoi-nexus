"""
Unit tests for Fuzzymon (Mega)
"""

import pytest

from fuzzymon.core import Fuzzymon
from fuzzymon.models import AnalysisResult, FuzzResult


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Fuzzymon"""
    return Fuzzymon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Fuzzymon"
        assert digimon.mission == "Fleeting Joy"
        assert digimon.role == "fuzz-tester"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"max_iterations": 500, "mutation_rate": 0.2}
        digimon = Fuzzymon(config=config)
        assert digimon.max_iterations == 500
        assert digimon.mutation_rate == 0.2


class TestFuzzing:
    """Tests para fuzzing"""

    def test_generate_fuzz_input(self, digimon):
        """Test generación de entrada fuzzed"""
        fuzz_input = digimon.generate_fuzz_input()
        assert isinstance(fuzz_input, str)
        assert len(fuzz_input) > 0

    def test_generate_fuzz_input_with_base(self, digimon):
        """Test generación de entrada con base"""
        base = "test input"
        fuzz_input = digimon.generate_fuzz_input(base)
        assert isinstance(fuzz_input, str)

    def test_fuzz_target(self, digimon):
        """Test fuzzing de objetivo"""
        result = digimon.fuzz_target()
        assert isinstance(result, FuzzResult)
        assert result.total_tests > 0


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_fuzzing(self, digimon):
        """Test analyze con fuzzing"""
        result = digimon.analyze(iterations=50)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_with_base_input(self, digimon):
        """Test analyze con entrada base"""
        result = digimon.analyze(base_input="test", iterations=50)
        assert isinstance(result, AnalysisResult)


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("test input") is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Fuzzymon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
