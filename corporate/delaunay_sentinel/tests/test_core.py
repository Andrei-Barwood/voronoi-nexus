"""
Unit tests for DelaunaySentinel (Production)
"""

import pytest

from delaunay_sentinel.core import DelaunaySentinel
from delaunay_sentinel.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return DelaunaySentinel()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Delaunay Sentinel"
        assert module.mission == "The Gunslinger"
        assert module.role == "malware-analyzer"

    def test_init_with_config(self):
        mod = DelaunaySentinel(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "suspicious_imports": 9,
    "packed_binary": True,
    "network_callbacks": 5,
    "anti_vm_checks": True,
}
        report = module.analyze_malware(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "suspicious_imports": 9,
    "packed_binary": True,
    "network_callbacks": 5,
    "anti_vm_checks": True,
}
        result = module.analyze(sample_data=data)
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
        assert info["name"] == "Delaunay Sentinel"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
