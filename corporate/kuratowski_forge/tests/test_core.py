"""
Unit tests for KuratowskiForge (Production)
"""

import pytest

from kuratowski_forge.core import KuratowskiForge
from kuratowski_forge.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return KuratowskiForge()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Kuratowski Forge"
        assert module.mission == "Red Dead Redemption"
        assert module.role == "disassembler"

    def test_init_with_config(self):
        mod = KuratowskiForge(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "indirect_jumps": 37,
    "opaque_predicates": 8,
    "control_flow_anomalies": 5,
    "anti_disassembly_tricks": True,
}
        report = module.disassemble_binary(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "indirect_jumps": 37,
    "opaque_predicates": 8,
    "control_flow_anomalies": 5,
    "anti_disassembly_tricks": True,
}
        result = module.analyze(binary_data=data)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning", "error"]


class TestValidation:
    def test_validate_none(self, module):
        assert module.validate(None) is False

    def test_validate_dict(self, module):
        assert module.validate({"k": "v"}) is True


class TestInfo:
    def test_get_info_returns_dict(self, module):
        info = module.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "Kuratowski Forge"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
