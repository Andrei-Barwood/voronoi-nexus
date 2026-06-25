"""Datos demo para evaluación de postura sin inventario real cargado."""

from __future__ import annotations

from typing import Any

# Valores representativos para una revisión inicial de infraestructura interna.
# Sustituir con --input infra-input.json al conectar datos reales.
INFRA_DEMO_INPUTS: dict[str, dict[str, Any]] = {
    "fractal_axiom": {
        "config_data": {
            "encryption_enabled": True,
            "logging_enabled": True,
            "mfa_enabled": True,
            "public_access": False,
        }
    },
    "vertex_stillness": {
        "vpc_data": {
            "flow_logs_enabled": True,
            "public_subnets": False,
            "network_acl_restrictive": True,
            "nat_gateway_configured": True,
        }
    },
    "hyperplane_guard": {
        "rules_data": {
            "default_deny": True,
            "open_ports": [443],
            "logging_enabled": True,
        }
    },
    "geodesic_network": {
        "connections": [
            {"source": "10.0.1.10", "destination": "10.0.2.5", "port": 443, "protocol": "tcp"},
            {"source": "10.0.1.99", "destination": "8.8.8.8", "port": 53, "protocol": "udp"},
        ]
    },
    "geodesic_identity": {
        "iam_data": {
            "wildcard_permissions": False,
            "mfa_enforced": True,
            "rotation_enabled": True,
            "inactive_users": 1,
        }
    },
    "lattice_permission": {
        "resources": [
            {"principal": "svc-build", "resource": "infra/cluster", "action": "read"},
            {"principal": "svc-deploy", "resource": "infra/cluster", "action": "write"},
        ]
    },
    "polytope_cluster": {
        "cluster_data": {
            "rbac_enabled": True,
            "network_policies": True,
            "pod_security_standard": "restricted",
            "audit_logging": True,
        }
    },
    "simplex_container": {
        "container_data": {
            "read_only_rootfs": True,
            "non_root_user": True,
            "capabilities_dropped": True,
            "image_scan_passed": True,
        }
    },
    "manifold_code": {
        "iac_data": {
            "encryption_at_rest": True,
            "public_exposure": False,
            "versioning_enabled": True,
            "least_privilege_iam": True,
        }
    },
    "lattice_resource": {
        "usage_data": {
            "cpu_utilization": 72,
            "memory_utilization": 68,
            "disk_utilization": 55,
            "gpu_utilization": 41,
        }
    },
    "torus_vault": {
        "bucket_data": {
            "public_access": False,
            "encryption_enabled": True,
            "versioning_enabled": True,
            "logging_enabled": True,
        }
    },
    "helix_vault": {
        "db_data": {
            "encryption_at_rest": True,
            "public_access": False,
            "backup_enabled": True,
            "audit_logging": True,
        }
    },
    "vertex_vuln": {
        "targets": ["build-farm-01.internal", "artifact-registry.internal"]
    },
    "lattice_policy": {
        "policy_check": {
            "policy_id": "infra-baseline",
            "required_controls": ["encryption", "logging", "mfa"],
            "enforced": True,
        }
    },
    "torus_log": {
        "log_lines": [
            "2026-06-25T10:00:00Z INFO auth login success user=build-agent",
            "2026-06-25T10:01:12Z WARN network connection external dns=8.8.8.8",
        ]
    },
    "helix_incident": {
        "incident_data": {
            "severity": "medium",
            "type": "unauthorized_access_attempt",
            "contained": True,
            "playbook_executed": True,
        }
    },
}


def demo_overrides_for(module: str) -> dict[str, Any]:
    return dict(INFRA_DEMO_INPUTS.get(module, {}))