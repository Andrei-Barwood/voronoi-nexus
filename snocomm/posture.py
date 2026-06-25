"""Infrastructure security posture assessment for internal hardware/cloud review."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from snocomm.manifest import ModuleMeta, load_manifest, resolve_module
from snocomm.posture_defaults import demo_overrides_for
from snocomm.runner import run_analyze

# Módulos orientados a postura de infraestructura interna (hardware, red, cloud, acceso).
INFRA_POSTURE_MODULES: list[dict[str, str]] = [
    {"module": "fractal_axiom", "category": "cloud_config", "focus": "Configuración cloud y hardening"},
    {"module": "vertex_stillness", "category": "network", "focus": "Segmentación VPC y red interna"},
    {"module": "hyperplane_guard", "category": "network", "focus": "Reglas de firewall y perímetro"},
    {"module": "geodesic_network", "category": "network", "focus": "Monitoreo de tráfico de red"},
    {"module": "geodesic_identity", "category": "access", "focus": "IAM y acceso a infraestructura"},
    {"module": "lattice_permission", "category": "access", "focus": "Permisos y least-privilege"},
    {"module": "polytope_cluster", "category": "compute", "focus": "Clústeres Kubernetes"},
    {"module": "simplex_container", "category": "compute", "focus": "Contenedores y runtime"},
    {"module": "manifold_code", "category": "iac", "focus": "Infraestructura como código (Terraform)"},
    {"module": "lattice_resource", "category": "hardware", "focus": "Uso de recursos y capacidad"},
    {"module": "torus_vault", "category": "storage", "focus": "Almacenamiento objeto (S3)"},
    {"module": "helix_vault", "category": "storage", "focus": "Bases de datos y persistencia"},
    {"module": "vertex_vuln", "category": "vulnerabilities", "focus": "Vulnerabilidades conocidas"},
    {"module": "vertex_scan", "category": "code", "focus": "Análisis estático de código"},
    {"module": "lattice_policy", "category": "governance", "focus": "Políticas de seguridad"},
    {"module": "torus_log", "category": "visibility", "focus": "Logs y trazabilidad"},
    {"module": "helix_incident", "category": "response", "focus": "Respuesta a incidentes"},
]

STATUS_SCORE = {
    "success": 100,
    "ok": 100,
    "warning": 60,
    "error": 0,
    "blocked": 0,
}


@dataclass
class PostureCheckResult:
    module: str
    display_name: str
    category: str
    focus: str
    status: str
    score: int
    message: str
    data: dict[str, Any]
    error: str | None = None


def _score_status(status: str) -> int:
    return STATUS_SCORE.get(status.lower(), 50)


def run_infra_posture(
    modules: list[ModuleMeta] | None = None,
    config: dict[str, Any] | None = None,
    input_overrides: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Ejecuta una evaluación de postura sobre módulos de infraestructura.

    Pensado para equipos que revisan la seguridad de infraestructura interna
    (red, hardware, acceso, almacenamiento, IaC).
    """
    catalog = modules or load_manifest()
    overrides_map = dict(input_overrides or {})
    checks: list[PostureCheckResult] = []
    used_demo_data = not bool(input_overrides)

    for spec in INFRA_POSTURE_MODULES:
        meta = resolve_module(spec["module"], catalog)
        if meta is None:
            checks.append(
                PostureCheckResult(
                    module=spec["module"],
                    display_name=spec["module"],
                    category=spec["category"],
                    focus=spec["focus"],
                    status="error",
                    score=0,
                    message="Módulo no encontrado en el catálogo",
                    data={},
                    error="not_in_manifest",
                )
            )
            continue

        try:
            module_overrides = demo_overrides_for(meta.folder_name)
            module_overrides.update(overrides_map.get(meta.folder_name, {}))
            payload = run_analyze(meta, config, module_overrides)
            result = payload["result"]
            status = str(result.get("status", "unknown")).lower()
            checks.append(
                PostureCheckResult(
                    module=meta.folder_name,
                    display_name=meta.display_name,
                    category=spec["category"],
                    focus=spec["focus"],
                    status=status,
                    score=_score_status(status),
                    message=str(result.get("message", "")),
                    data=result.get("data") or {},
                )
            )
        except Exception as exc:
            checks.append(
                PostureCheckResult(
                    module=meta.folder_name,
                    display_name=meta.display_name,
                    category=spec["category"],
                    focus=spec["focus"],
                    status="error",
                    score=0,
                    message="Fallo al ejecutar el módulo",
                    data={},
                    error=str(exc),
                )
            )

    if checks:
        overall_score = round(sum(c.score for c in checks) / len(checks), 1)
    else:
        overall_score = 0.0

    failed = [c for c in checks if c.status in {"error", "blocked"}]
    warnings = [c for c in checks if c.status == "warning"]

    if overall_score >= 85 and not failed:
        posture_level = "STRONG"
    elif overall_score >= 65:
        posture_level = "MODERATE"
    else:
        posture_level = "NEEDS_ATTENTION"

    categories: dict[str, Any] = {}
    for check in checks:
        bucket = categories.setdefault(
            check.category,
            {"checks": [], "score": 0.0, "count": 0},
        )
        bucket["checks"].append(
            {
                "module": check.module,
                "display_name": check.display_name,
                "status": check.status,
                "score": check.score,
                "focus": check.focus,
                "message": check.message,
                "error": check.error,
            }
        )
        bucket["count"] += 1

    for bucket in categories.values():
        bucket["score"] = round(
            sum(item["score"] for item in bucket["checks"]) / bucket["count"],
            1,
        )

    return {
        "report_type": "infrastructure_security_posture",
        "audience": "internal_infrastructure_review",
        "data_mode": "demo_baseline" if used_demo_data else "custom_input",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "overall_score": overall_score,
        "posture_level": posture_level,
        "summary": {
            "total_checks": len(checks),
            "passed": len([c for c in checks if c.status in {"success", "ok"}]),
            "warnings": len(warnings),
            "failed": len(failed),
        },
        "priority_actions": [
            {
                "module": c.display_name,
                "category": c.category,
                "reason": c.message or c.error or c.status,
            }
            for c in sorted(checks, key=lambda x: x.score)[:5]
            if c.score < 85
        ],
        "categories": categories,
        "checks": [
            {
                "module": c.module,
                "display_name": c.display_name,
                "category": c.category,
                "focus": c.focus,
                "status": c.status,
                "score": c.score,
                "message": c.message,
                "data": c.data,
                "error": c.error,
            }
            for c in checks
        ],
    }