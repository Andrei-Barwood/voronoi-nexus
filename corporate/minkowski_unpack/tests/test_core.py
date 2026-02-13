"""
Unit tests for MinkowskiUnpack (Production)
"""

import pytest

from minkowski_unpack.core import MinkowskiUnpack
from minkowski_unpack.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return MinkowskiUnpack()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Minkowski Unpack"
        assert module.mission == "Clemens Point"
        assert module.role == "packer-analyzer"

    def test_init_with_config(self):
        mod = MinkowskiUnpack(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "section_entropy": 7.9,
    "suspicious_stub_detected": True,
    "runtime_unpack_behavior": True,
    "overlay_size_kb": 620,
}
        report = module.analyze_packer(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "section_entropy": 7.9,
    "suspicious_stub_detected": True,
    "runtime_unpack_behavior": True,
    "overlay_size_kb": 620,
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
        assert info["name"] == "Minkowski Unpack"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
