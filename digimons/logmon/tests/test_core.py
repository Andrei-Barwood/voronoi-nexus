"""
Unit tests for Logmon (Mega)
"""

import pytest

from logmon.core import Logmon
from logmon.models import AnalysisResult, LogAnalysis


@pytest.fixture
def digimon():
    """Fixture para crear instancia de Logmon"""
    return Logmon()


class TestInitialization:
    """Tests para inicialización"""

    def test_init_default(self, digimon):
        """Test inicialización con valores por defecto"""
        assert digimon.name == "Logmon"
        assert digimon.mission == "Goodbye, Dear Friend"
        assert digimon.role == "log-analyzer"

    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"log_levels": ["ERROR", "WARN"], "correlation_window": 600}
        digimon = Logmon(config=config)
        assert len(digimon.log_levels) == 2
        assert digimon.correlation_window == 600


class TestLogParsing:
    """Tests para parsing de logs"""

    def test_parse_log_entry(self, digimon):
        """Test parsear entrada de log"""
        log_line = "2025-01-15 10:30:45 ERROR Connection failed"
        entry = digimon.parse_log_entry(log_line)
        assert entry is not None
        assert entry.level == "ERROR"

    def test_analyze_logs(self, digimon):
        """Test análisis de logs"""
        log_lines = [
            "2025-01-15 10:30:45 ERROR Connection failed",
            "2025-01-15 10:31:00 WARN High memory usage",
        ]
        analysis = digimon.analyze_logs(log_lines)
        assert isinstance(analysis, LogAnalysis)
        assert analysis.total_entries == 2


class TestAnalyze:
    """Tests para funcionalidad de análisis"""

    def test_analyze_with_string(self, digimon):
        """Test analyze con string"""
        log_data = "2025-01-15 10:30:45 ERROR Connection failed\n2025-01-15 10:31:00 INFO Operation completed"
        result = digimon.analyze(log_data=log_data)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning"]

    def test_analyze_with_list(self, digimon):
        """Test analyze con lista"""
        log_lines = ["2025-01-15 10:30:45 ERROR Connection failed"]
        result = digimon.analyze(log_lines=log_lines)
        assert isinstance(result, AnalysisResult)

    def test_analyze_no_input(self, digimon):
        """Test analyze sin input"""
        result = digimon.analyze()
        assert result.status == "error"


class TestValidation:
    """Tests para validación"""

    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False

    def test_validate_str(self, digimon):
        """Test validación con string"""
        assert digimon.validate("log line") is True

    def test_validate_list(self, digimon):
        """Test validación con lista"""
        assert digimon.validate(["log1", "log2"]) is True


class TestInfo:
    """Tests para información del Digimon"""

    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Logmon"
        assert info["status"] == "Mega"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
