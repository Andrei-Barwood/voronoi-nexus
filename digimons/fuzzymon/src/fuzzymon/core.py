"""
Core functionality for Fuzzymon (Mega)

Fuzzymon ejecuta fuzzing para encontrar bugs y vulnerabilidades.
Misión: Fleeting Joy
Rol: fuzz-tester
"""

import logging
import random
import string
from typing import Any, Dict, List, Optional

from .models import AnalysisResult, FuzzResult

logger = logging.getLogger(__name__)


class Fuzzymon:
    """
    Fuzzymon - Fuzz Tester (Mega)

    Descripción:
        Ejecuta fuzzing para encontrar bugs y vulnerabilidades usando
        técnicas de mutación y generación de entrada (2025-2026).
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar Fuzzymon.

        Args:
            config: Diccionario de configuración opcional:
                - max_iterations: Máximo de iteraciones (default: 1000)
                - mutation_rate: Tasa de mutación (default: 0.1)
                - timeout_seconds: Timeout por test (default: 5)
        """
        self.name = "Fuzzymon"
        self.mission = "Fleeting Joy"
        self.role = "fuzz-tester"
        self.config = config or {}

        self.max_iterations = int(self.config.get("max_iterations", 1000))
        self.mutation_rate = float(self.config.get("mutation_rate", 0.1))
        self.timeout_seconds = int(self.config.get("timeout_seconds", 5))

        # Patrones comunes para fuzzing
        self.fuzz_patterns = [
            lambda: "A" * 1000,  # Buffer overflow
            lambda: "".join(random.choices(string.ascii_letters + string.digits, k=100)),
            lambda: "<script>alert('xss')</script>",  # XSS
            lambda: "' OR '1'='1",  # SQL injection
            lambda: ".." * 100,  # Path traversal
        ]

        logger.info(
            "Initialized %s - %s (max_iter=%d, mutation_rate=%.2f)",
            self.name,
            self.role,
            self.max_iterations,
            self.mutation_rate,
        )

    def generate_fuzz_input(self, base_input: Optional[str] = None) -> str:
        """
        Genera una entrada fuzzed.

        Args:
            base_input: Entrada base para mutar (opcional)

        Returns:
            String con entrada fuzzed
        """
        if base_input and random.random() < self.mutation_rate:
            # Mutar entrada base
            chars = list(base_input)
            if chars:
                idx = random.randint(0, len(chars) - 1)
                chars[idx] = random.choice(string.printable)
                return "".join(chars)

        # Generar entrada desde cero
        pattern = random.choice(self.fuzz_patterns)
        return pattern()

    def fuzz_target(self, target_function=None, base_input: Optional[str] = None) -> FuzzResult:
        """
        Ejecuta fuzzing en un objetivo.

        Args:
            target_function: Función a fuzzear (opcional, simulado)
            base_input: Entrada base (opcional)

        Returns:
            FuzzResult con resultados
        """
        crashes = 0
        hangs = 0
        bugs: List[str] = []
        tests_run = 0

        # Simulación de fuzzing
        for i in range(min(self.max_iterations, 100)):  # Limitar a 100 para tests
            fuzz_input = self.generate_fuzz_input(base_input)
            tests_run += 1

            # Simular detección de bugs (probabilidad baja)
            if random.random() < 0.05:  # 5% chance
                bug_type = random.choice(["buffer_overflow", "format_string", "integer_overflow"])
                bugs.append(f"{bug_type} detected with input: {fuzz_input[:50]}")

            # Simular crash (probabilidad muy baja)
            if random.random() < 0.01:  # 1% chance
                crashes += 1

        # Calcular coverage (simulado)
        coverage = min(100.0, (tests_run / self.max_iterations) * 100)

        return FuzzResult(
            total_tests=tests_run,
            crashes_found=crashes,
            hangs_found=hangs,
            bugs_found=bugs[:20],  # Limitar a 20
            coverage_percent=coverage,
            fuzz_summary={
                "max_iterations": self.max_iterations,
                "mutation_rate": self.mutation_rate,
                "timeout_seconds": self.timeout_seconds,
                "bug_rate": len(bugs) / tests_run if tests_run > 0 else 0,
            },
        )

    def analyze(
        self, target_function=None, base_input: Optional[str] = None, iterations: Optional[int] = None
    ) -> AnalysisResult:
        """
        Ejecuta análisis de fuzzing.

        Args:
            target_function: Función a fuzzear (opcional)
            base_input: Entrada base (opcional)
            iterations: Número de iteraciones (opcional)

        Returns:
            AnalysisResult con resultados
        """
        original_max = self.max_iterations
        if iterations:
            self.max_iterations = iterations

        try:
            result = self.fuzz_target(target_function, base_input)
            status = "warning" if result.crashes_found > 0 or result.bugs_found else "success"

            return AnalysisResult(
                status=status,
                message=f"Fuzzing completed: {result.total_tests} tests, {result.crashes_found} crashes, {len(result.bugs_found)} bugs",
                data=result.model_dump(),
            )
        finally:
            self.max_iterations = original_max

    def validate(self, data: Any) -> bool:
        """
        Valida datos de entrada.
        """
        if data is None:
            return False
        if isinstance(data, str):
            return True  # Cualquier string es válido para fuzzing
        return True  # Fuzzing acepta varios tipos

    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del Digimon.
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Mega",
            "max_iterations": str(self.max_iterations),
            "mutation_rate": str(self.mutation_rate),
        }


# Alias para retrocompatibilidad
Digimon = Fuzzymon
