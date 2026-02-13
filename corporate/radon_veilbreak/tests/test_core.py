"""
Unit tests for RadonVeilbreak (Production)
"""

import pytest

from radon_veilbreak.core import RadonVeilbreak
from radon_veilbreak.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return RadonVeilbreak()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Radon Veilbreak"
        assert module.mission == "Paradise Mercifully Departed"
        assert module.role == "steganography-detector"

    def test_init_with_config(self):
        mod = RadonVeilbreak(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "lsb_irregularity_score": 0.81,
    "container_mismatch": True,
    "payload_signature_hits": 3,
    "metadata_anomaly": True,
}
        report = module.detect_steganography(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "lsb_irregularity_score": 0.81,
    "container_mismatch": True,
    "payload_signature_hits": 3,
    "metadata_anomaly": True,
}
        result = module.analyze(artifact_data=data)
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
        assert info["name"] == "Radon Veilbreak"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
