"""
Unit tests for HausdorffMatch (Production)
"""

import pytest

from hausdorff_match.core import HausdorffMatch
from hausdorff_match.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return HausdorffMatch()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Hausdorff Match"
        assert module.mission == "My Last Boy"
        assert module.role == "signature-matcher"

    def test_init_with_config(self):
        mod = HausdorffMatch(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "known_signature_hits": 6,
    "fuzzy_match_ratio": 0.84,
    "variant_clusters": 2,
    "collision_suspected": False,
}
        report = module.match_signatures(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "known_signature_hits": 6,
    "fuzzy_match_ratio": 0.84,
    "variant_clusters": 2,
    "collision_suspected": False,
}
        result = module.analyze(signature_data=data)
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
        assert info["name"] == "Hausdorff Match"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
