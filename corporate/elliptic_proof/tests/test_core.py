"""
Unit tests for EllipticProof (Production)
"""

import pytest

from elliptic_proof.core import EllipticProof
from elliptic_proof.models import AnalysisResult, DetectionReport


@pytest.fixture
def module():
    return EllipticProof()


class TestInitialization:
    def test_init_default(self, module):
        assert module.name == "Elliptic Proof"
        assert module.mission == "Good Intentions"
        assert module.role == "crypto-analyzer"

    def test_init_with_config(self):
        mod = EllipticProof(config={"severity_threshold": "high", "confidence_threshold": 0.5})
        assert mod.severity_threshold == "high"
        assert mod.confidence_threshold == 0.5


class TestPrimaryMethod:
    def test_primary_method(self, module):
        data = {
    "deprecated_ciphers": 2,
    "weak_key_detected": True,
    "tls_misconfigurations": 4,
    "signature_validation_issues": 1,
}
        report = module.analyze_cryptography(data)
        assert isinstance(report, DetectionReport)
        assert report.total_checks > 0


class TestAnalyze:
    def test_analyze(self, module):
        data = {
    "deprecated_ciphers": 2,
    "weak_key_detected": True,
    "tls_misconfigurations": 4,
    "signature_validation_issues": 1,
}
        result = module.analyze(crypto_data=data)
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
        assert info["name"] == "Elliptic Proof"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
