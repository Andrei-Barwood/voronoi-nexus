"""
Core functionality for MFAmon (Mega)

MFAmon implementa autenticación multifactor con múltiples métodos.
Misión: Red Dead Redemption
Rol: mfa-enforcer
"""

import logging
import secrets
import time
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, MFAAnalysis, MFAChallenge

logger = logging.getLogger(__name__)


class MFAmon:
    """
    MFAmon - MFA Enforcer (Mega)

    Descripción:
        Implementa autenticación multifactor con TOTP, SMS, email,
        push notifications y verificación de códigos (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar MFAmon.

        Args:
            config: Diccionario de configuración opcional:
                - mfa_methods: Métodos soportados (default: totp, sms, email, push)
                - default_method: Método por defecto (default: "totp")
                - code_expiry: Expiración de código en segundos (default: 300)
                - max_attempts: Máximo de intentos (default: 3)
        """
        self.name = "MFAmon"
        self.mission = "Red Dead Redemption"
        self.role = "mfa-enforcer"
        self.config = config or {}

        self.mfa_methods = self.config.get("mfa_methods", ["totp", "sms", "email", "push"])
        self.default_method = self.config.get("default_method", "totp")
        self.code_expiry = int(self.config.get("code_expiry", 300))
        self.max_attempts = int(self.config.get("max_attempts", 3))

        # Simulación de almacenamiento de desafíos (en producción usar DB/Redis)
        self.challenges: Dict[str, Dict[str, Any]] = {}

        logger.info(
            "Initialized %s - %s (methods=%s, default=%s, expiry=%ds)",
            self.name,
            self.role,
            len(self.mfa_methods),
            self.default_method,
            self.code_expiry,
        )

    def generate_code(self, length: int = 6) -> str:
        """Genera código numérico para MFA."""
        return "".join([str(secrets.randbelow(10)) for _ in range(length)])

    def create_challenge(self, user_id: str, method: Optional[str] = None) -> MFAChallenge:
        """
        Crea un desafío MFA.

        Args:
            user_id: ID del usuario
            method: Método MFA (opcional, usa default si no se especifica)

        Returns:
            MFAChallenge creado
        """
        mfa_method = method or self.default_method
        if mfa_method not in self.mfa_methods:
            raise ValueError(f"Unsupported MFA method: {mfa_method}")

        challenge_id = secrets.token_urlsafe(16)
        now = datetime.now()
        expires_at = now + timedelta(seconds=self.code_expiry)

        # Generar código (solo para métodos que lo requieren)
        code = None
        if mfa_method in ["totp", "sms", "email"]:
            code = self.generate_code()

        challenge_data = {
            "challenge_id": challenge_id,
            "user_id": user_id,
            "method": mfa_method,
            "code": code,
            "expires_at": expires_at.isoformat(),
            "verified": False,
            "attempts": 0,
            "expires_timestamp": expires_at.timestamp(),
        }
        self.challenges[challenge_id] = challenge_data

        return MFAChallenge(
            challenge_id=challenge_id,
            user_id=user_id,
            method=mfa_method,
            code=code,  # En producción no se expone
            expires_at=expires_at.isoformat(),
            verified=False,
            attempts=0,
        )

    def verify_challenge(self, challenge_id: str, code: str) -> bool:
        """
        Verifica un código MFA.

        Args:
            challenge_id: ID del desafío
            code: Código a verificar

        Returns:
            True si el código es válido
        """
        if challenge_id not in self.challenges:
            return False

        challenge = self.challenges[challenge_id]

        # Verificar expiración
        if time.time() > challenge.get("expires_timestamp", 0):
            self.challenges.pop(challenge_id, None)
            return False

        # Verificar intentos
        attempts = challenge.get("attempts", 0)
        if attempts >= self.max_attempts:
            self.challenges.pop(challenge_id, None)
            return False

        # Verificar código
        expected_code = challenge.get("code")
        challenge["attempts"] = attempts + 1

        if code == expected_code:
            challenge["verified"] = True
            return True

        return False

    def analyze_mfa(self) -> MFAAnalysis:
        """
        Analiza todos los desafíos MFA.

        Returns:
            MFAAnalysis con resultados
        """
        verified = 0
        pending = 0
        failed = 0
        methods_usage: Dict[str, int] = defaultdict(int)
        violations: List[str] = []

        now_timestamp = time.time()

        for challenge_data in list(self.challenges.values()):
            method = challenge_data.get("method", "unknown")
            methods_usage[method] += 1

            expires_timestamp = challenge_data.get("expires_timestamp", 0)
            if now_timestamp > expires_timestamp:
                failed += 1
                self.challenges.pop(challenge_data.get("challenge_id"), None)
            elif challenge_data.get("verified", False):
                verified += 1
            else:
                pending += 1

            # Verificar violaciones
            attempts = challenge_data.get("attempts", 0)
            if attempts >= self.max_attempts:
                violations.append(f"Challenge {challenge_data.get('challenge_id')} exceeded max attempts")

        return MFAAnalysis(
            total_challenges=len(self.challenges),
            verified_count=verified,
            pending_count=pending,
            failed_count=failed,
            methods_usage=dict(methods_usage),
            violations=violations,
            analysis_summary={
                "code_expiry": self.code_expiry,
                "max_attempts": self.max_attempts,
                "violation_count": len(violations),
            },
        )

    def analyze(self, action: str = "analyze", challenge_data: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: analizar MFA o crear desafío.

        Args:
            action: Acción ("analyze" o "create")
            challenge_data: Datos del desafío (si action="create")

        Returns:
            AnalysisResult con resultados
        """
        if action == "analyze":
            analysis = self.analyze_mfa()
            status = "warning" if analysis.violations else "success"
            return AnalysisResult(
                status=status,
                message=f"MFA analysis completed: {analysis.total_challenges} challenges",
                data=analysis.model_dump(),
            )

        elif action == "create" and challenge_data:
            try:
                user_id = challenge_data.get("user_id", "")
                method = challenge_data.get("method")
                challenge = self.create_challenge(user_id, method)
                return AnalysisResult(
                    status="success",
                    message="MFA challenge created successfully",
                    data=challenge.model_dump(),
                )
            except Exception as e:
                return AnalysisResult(
                    status="error",
                    message="MFA challenge creation failed",
                    data={},
                    errors=[str(e)],
                )

        return AnalysisResult(
            status="error",
            message="Invalid action or missing parameters",
            data={},
            errors=["invalid_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, dict):
            return "user_id" in data
        return True

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "mfa_methods": ", ".join(self.mfa_methods),
            "default_method": self.default_method,
        }


# Alias para retrocompatibilidad
Digimon = MFAmon

