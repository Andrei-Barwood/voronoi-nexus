"""
Unit tests for AffineReplica (Production)
"""

import pytest

from affine_replica.core import AffineReplica
from affine_replica.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return AffineReplica()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Affine Replica"
        assert module.mission == "American Distillation"
        assert module.role == "emulation-engine"

    def test_init_with_config(self):
        mod = AffineReplica(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "api_sequence_similarity": 0.88,
    "syscall_profile_risk": 0.73,
    "evasion_signals": 3,
    "payload_stage_count": 2,
}
        report = module.emulate_behavior(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "api_sequence_similarity": 0.88,
    "syscall_profile_risk": 0.73,
    "evasion_signals": 3,
    "payload_stage_count": 2,
}
        result = module.analyze(execution_data=data)
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
        assert info["name"] == "Affine Replica"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
