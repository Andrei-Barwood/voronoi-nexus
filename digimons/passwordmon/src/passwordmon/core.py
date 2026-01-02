"""
Core functionality for Passwordmon (Mega)

Passwordmon valida robustez de contraseñas con políticas avanzadas.
Misión: The Gilded Cage
Rol: password-validator
"""

import logging
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, PasswordValidation

logger = logging.getLogger(__name__)


class Passwordmon:
    """
    Passwordmon - Password Validator (Mega)

    Descripción:
        Valida robustez de contraseñas aplicando políticas estrictas,
        verificación contra contraseñas comunes y cálculo de fuerza (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Passwordmon.

        Args:
            config: Diccionario de configuración opcional:
                - min_length: Longitud mínima (default: 12)
                - require_uppercase: Requerir mayúsculas (default: True)
                - require_lowercase: Requerir minúsculas (default: True)
                - require_numbers: Requerir números (default: True)
                - require_special: Requerir caracteres especiales (default: True)
                - check_common_passwords: Verificar contraseñas comunes (default: True)
        """
        self.name = "Passwordmon"
        self.mission = "The Gilded Cage"
        self.role = "password-validator"
        self.config = config or {}

        self.min_length = int(self.config.get("min_length", 12))
        self.require_uppercase = bool(self.config.get("require_uppercase", True))
        self.require_lowercase = bool(self.config.get("require_lowercase", True))
        self.require_numbers = bool(self.config.get("require_numbers", True))
        self.require_special = bool(self.config.get("require_special", True))
        self.check_common_passwords = bool(self.config.get("check_common_passwords", True))

        # Lista de contraseñas comunes (simplificado)
        self.common_passwords = {
            "password",
            "12345678",
            "123456789",
            "qwerty",
            "abc123",
            "password123",
        }

        logger.info(
            "Initialized %s - %s (min_length=%d, check_common=%s)",
            self.name,
            self.role,
            self.min_length,
            self.check_common_passwords,
        )

    def validate_password(self, password: str) -> PasswordValidation:
        """
        Valida una contraseña.

        Args:
            password: Contraseña a validar

        Returns:
            PasswordValidation con resultado
        """
        violations: List[str] = []
        recommendations: List[str] = []
        score = 0

        # Longitud
        if len(password) < self.min_length:
            violations.append(f"Password length < {self.min_length} characters")
        else:
            score += 20

        # Mayúsculas
        if self.require_uppercase:
            if not any(c.isupper() for c in password):
                violations.append("Missing uppercase letter")
            else:
                score += 20

        # Minúsculas
        if self.require_lowercase:
            if not any(c.islower() for c in password):
                violations.append("Missing lowercase letter")
            else:
                score += 20

        # Números
        if self.require_numbers:
            if not any(c.isdigit() for c in password):
                violations.append("Missing number")
            else:
                score += 20

        # Especiales
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if self.require_special:
            if not any(c in special_chars for c in password):
                violations.append("Missing special character")
            else:
                score += 20

        # Contraseñas comunes
        if self.check_common_passwords and password.lower() in self.common_passwords:
            violations.append("Password is too common")
            score = max(0, score - 30)

        # Longitud extra para score
        if len(password) >= 16:
            score += 10
        if len(password) >= 20:
            score += 10

        score = min(100, max(0, score))

        # Determinar fuerza
        if score >= 80:
            strength = "strong"
        elif score >= 50:
            strength = "medium"
        else:
            strength = "weak"

        # Recomendaciones
        if len(violations) > 0:
            recommendations.append("Fix all validation violations")
        if score < 80:
            recommendations.append("Use a longer password (16+ characters)")
            recommendations.append("Avoid common words and patterns")

        valid = len(violations) == 0

        return PasswordValidation(
            password="*" * len(password),  # No exponer contraseña
            valid=valid,
            strength=strength,
            score=score,
            violations=violations,
            recommendations=recommendations,
        )

    def analyze(self, password: Optional[str] = None, passwords: Optional[List[str]] = None) -> AnalysisResult:
        """
        Ejecuta análisis: una contraseña o múltiples.

        Args:
            password: Contraseña individual
            passwords: Lista de contraseñas

        Returns:
            AnalysisResult con resultados
        """
        if passwords:
            validations = []
            valid_count = 0
            for pwd in passwords:
                validation = self.validate_password(pwd)
                validations.append(validation.model_dump())
                if validation.valid:
                    valid_count += 1

            status = "success" if valid_count == len(passwords) else "warning"
            return AnalysisResult(
                status=status,
                message=f"Validated {len(passwords)} passwords: {valid_count} valid",
                data={"validations": validations, "total": len(passwords), "valid": valid_count},
            )

        elif password:
            validation = self.validate_password(password)
            status = "success" if validation.valid else "warning"
            return AnalysisResult(
                status=status,
                message=f"Password validation: {validation.strength}",
                data=validation.model_dump(),
            )

        return AnalysisResult(
            status="error",
            message="No password provided",
            data={},
            errors=["missing_input"],
        )

    def validate(self, data: Any) -> bool:
        """Valida datos de entrada."""
        if data is None:
            return False
        if isinstance(data, str):
            return bool(data)
        if isinstance(data, list):
            return all(isinstance(item, str) and item for item in data)
        return False

    def get_info(self) -> Dict[str, str]:
        """Obtener información del Digimon."""
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "min_length": str(self.min_length),
            "require_special": str(self.require_special),
        }


# Alias para retrocompatibilidad
Digimon = Passwordmon

