#!/usr/bin/env python3
"""
Generate tests, docs, examples, and pyproject for Block 5 corporate.

Skips files that already exist.
"""

from pathlib import Path


MODULES = [
    {
        "name": "cloudsecmon",
        "class_name": "CloudSecmon",
        "mission": "American Venom",
        "role_display": "Cloud Config Auditor",
        "role_code": "cloud-config-auditor",
        "description": "Audita configuraciones cloud con controles basicos.",
        "analyze_arg": "config_data",
        "audit_method": "audit_config",
        "audit_label": "configuracion cloud",
        "sample_data": """{
    "encryption_enabled": True,
    "logging_enabled": True,
    "mfa_enabled": True,
    "public_access": False,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `severity_threshold`: Severidad minima a reportar",
            "- `require_encryption`: Requerir cifrado en reposo",
            "- `require_logging`: Requerir logging habilitado",
            "- `require_mfa`: Requerir MFA para administradores",
        ],
    },
    {
        "name": "iammon",
        "class_name": "IAMmon",
        "mission": "Charlotte Balfour",
        "role_display": "IAM Analyzer",
        "role_code": "iam-analyzer",
        "description": "Analiza configuraciones IAM y permisos.",
        "analyze_arg": "iam_data",
        "audit_method": "audit_iam",
        "audit_label": "IAM",
        "sample_data": """{
    "wildcard_permissions": False,
    "mfa_enforced": True,
    "rotation_enabled": True,
    "inactive_users": 0,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `severity_threshold`: Severidad minima a reportar",
            "- `require_mfa`: Requerir MFA en usuarios privilegiados",
            "- `require_rotation`: Requerir rotacion de llaves",
            "- `max_inactive_users`: Maximo de usuarios inactivos permitidos",
        ],
    },
    {
        "name": "vpcmon",
        "class_name": "VPCmon",
        "mission": "Outlaws from the West",
        "role_display": "VPC Monitor",
        "role_code": "vpc-monitor",
        "description": "Monitorea configuraciones de redes privadas.",
        "analyze_arg": "vpc_data",
        "audit_method": "audit_vpc",
        "audit_label": "VPC",
        "sample_data": """{
    "flow_logs_enabled": True,
    "public_subnets": False,
    "network_acl_restrictive": True,
    "nat_gateway_configured": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `require_flow_logs`: Requerir flow logs habilitados",
            "- `require_nat_gateway`: Requerir NAT gateway",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "firewallguard",
        "class_name": "FirewallGuard",
        "mission": "Good, Honest Snake Oil",
        "role_display": "Firewall Manager",
        "role_code": "firewall-manager",
        "description": "Gestiona y audita reglas de firewall.",
        "analyze_arg": "rules_data",
        "audit_method": "audit_rules",
        "audit_label": "reglas de firewall",
        "sample_data": """{
    "default_deny": True,
    "open_ports": [80, 443],
    "logging_enabled": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `allowed_ports`: Lista de puertos permitidos",
            "- `require_logging`: Requerir logging de firewall",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "s3mon",
        "class_name": "S3mon",
        "mission": "Paradise Mercifully Departed",
        "role_display": "S3 Auditor",
        "role_code": "s3-auditor",
        "description": "Audita buckets S3 con controles de seguridad.",
        "analyze_arg": "bucket_data",
        "audit_method": "audit_bucket",
        "audit_label": "bucket",
        "sample_data": """{
    "public_access": False,
    "encryption_enabled": True,
    "versioning_enabled": True,
    "logging_enabled": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `require_encryption`: Requerir cifrado en buckets",
            "- `require_versioning`: Requerir versionado",
            "- `require_logging`: Requerir logging de acceso",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "rdsmon",
        "class_name": "RDSmon",
        "mission": "The Noblest of Men",
        "role_display": "Database Auditor",
        "role_code": "database-auditor",
        "description": "Audita bases de datos cloud con controles basicos.",
        "analyze_arg": "db_data",
        "audit_method": "audit_database",
        "audit_label": "base de datos",
        "sample_data": """{
    "public_access": False,
    "storage_encrypted": True,
    "backup_retention_days": 7,
    "multi_az": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `min_backup_retention_days`: Minimo de dias de retencion",
            "- `require_encryption`: Requerir cifrado en storage",
            "- `require_multi_az`: Requerir despliegue Multi-AZ",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "kubernetesmon",
        "class_name": "Kubernetesmon",
        "mission": "Fleeting Joy",
        "role_display": "K8s Scanner",
        "role_code": "k8s-scanner",
        "description": "Escanea clusters Kubernetes con controles de seguridad.",
        "analyze_arg": "cluster_data",
        "audit_method": "scan_cluster",
        "audit_label": "cluster Kubernetes",
        "sample_data": """{
    "rbac_enabled": True,
    "pod_security_policies": True,
    "etcd_encryption": True,
    "public_api": False,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `require_rbac`: Requerir RBAC habilitado",
            "- `require_psp`: Requerir pod security policies",
            "- `require_etcd_encryption`: Requerir cifrado en etcd",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "dockermon",
        "class_name": "Dockermon",
        "mission": "A Kind and benevolent Despot",
        "role_display": "Docker Auditor",
        "role_code": "docker-auditor",
        "description": "Audita contenedores Docker con controles basicos.",
        "analyze_arg": "container_data",
        "audit_method": "audit_container",
        "audit_label": "contenedor",
        "sample_data": """{
    "run_as_root": False,
    "privileged": False,
    "read_only_fs": True,
    "signed_images": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `require_signed_images`: Requerir imagenes firmadas",
            "- `require_read_only_fs`: Requerir filesystem read-only",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "terraformmon",
        "class_name": "Terraformmon",
        "mission": "Red Dead Redemption",
        "role_display": "IaC Validator",
        "role_code": "iac-validator",
        "description": "Valida Infrastructure as Code con controles basicos.",
        "analyze_arg": "iac_data",
        "audit_method": "validate_iac",
        "audit_label": "IaC",
        "sample_data": """{
    "contains_hardcoded_secrets": False,
    "remote_state_encrypted": True,
    "plan_approved": True,
    "modules_pinned": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `require_remote_state_encrypted`: Requerir cifrado del state",
            "- `require_plan_approval`: Requerir aprobacion del plan",
            "- `require_modules_pinned`: Requerir versiones fijadas",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "resourcemon",
        "class_name": "Resourcemon",
        "mission": "American Distillation",
        "role_display": "Resource Limiter",
        "role_code": "resource-limiter",
        "description": "Limita uso de recursos y detecta excesos.",
        "analyze_arg": "usage_data",
        "audit_method": "audit_usage",
        "audit_label": "uso de recursos",
        "sample_data": """{
    "cpu_usage": 40,
    "memory_usage": 35,
    "storage_usage": 50,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `max_cpu_percent`: Maximo de CPU permitido",
            "- `max_memory_percent`: Maximo de memoria permitida",
            "- `max_storage_percent`: Maximo de storage permitido",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "compliancecloud",
        "class_name": "ComplianceCloud",
        "mission": "Good Intentions",
        "role_display": "Cloud Compliance",
        "role_code": "cloud-compliance",
        "description": "Audita cumplimiento en cloud con controles basicos.",
        "analyze_arg": "compliance_data",
        "audit_method": "audit_compliance",
        "audit_label": "cumplimiento",
        "sample_data": """{
    "passed_controls": 3,
    "evidence_collected": True,
    "continuous_monitoring": True,
    "frameworks_checked": ["SOC2"],
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `min_passed_controls`: Controles minimos aprobados",
            "- `require_evidence`: Requerir evidencia de cumplimiento",
            "- `require_continuous_monitoring`: Requerir monitoreo continuo",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "costmonitor",
        "class_name": "CostMonitor",
        "mission": "The Gilded Cage",
        "role_display": "Cost Optimizer",
        "role_code": "cost-optimizer",
        "description": "Optimiza costos de seguridad en cloud.",
        "analyze_arg": "cost_data",
        "audit_method": "audit_costs",
        "audit_label": "costos",
        "sample_data": """{
    "cost_anomalies": 0,
    "idle_resources": 0,
    "budget_guardrails": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `max_idle_resources`: Maximo de recursos ociosos",
            "- `max_cost_anomalies`: Maximo de anomalias permitidas",
            "- `require_budget_guardrails`: Requerir guardrails de presupuesto",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
    {
        "name": "backupcloud",
        "class_name": "BackupCloud",
        "mission": "My Last Boy",
        "role_display": "Cloud Backup Auditor",
        "role_code": "cloud-backup-auditor",
        "description": "Audita backups en cloud con controles basicos.",
        "analyze_arg": "backup_data",
        "audit_method": "audit_backups",
        "audit_label": "backups",
        "sample_data": """{
    "backup_enabled": True,
    "backup_retention_days": 7,
    "last_backup_hours": 6,
    "cross_region_replication": True,
}""",
        "config_params": [
            "- `strict_mode`: Si True, falla ante settings criticos faltantes",
            "- `min_retention_days`: Dias minimos de retencion",
            "- `max_backup_age_hours`: Maximo de horas desde el ultimo backup",
            "- `require_cross_region`: Requerir replicacion cross-region",
            "- `severity_threshold`: Severidad minima a reportar",
        ],
    },
]


PYPROJECT_TEMPLATE = """[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[project]
name = "{name}"
version = "3.0.0"
description = "{description} (Production)"
readme = "README.md"
license = {{text = "MIT"}}
authors = [{{name = "Kirtan Teg Singh", email = "security@snocomm.dev"}}]
requires-python = ">=3.10"
keywords = ["cybersecurity", "modulo", "{name}"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Security",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "pydantic>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.4.0",
    "isort>=5.12.0",
]
docs = [
    "sphinx>=7.0.0",
    "sphinx-rtd-theme>=1.3.0",
    "sphinx-autodoc-typehints>=1.24.0",
]

[project.urls]
Homepage = "https://github.com/Andrei-Barwood/voronoi-nexus"
Documentation = "https://github.com/Andrei-Barwood/voronoi-nexus#readme"
Repository = "https://github.com/Andrei-Barwood/voronoi-nexus/tree/main/corporate/{name}"
Issues = "https://github.com/Andrei-Barwood/voronoi-nexus/issues"

[tool.poetry]
packages = [{{include = "{name}", from = "src"}}]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--strict-markers"
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
]

[tool.black]
line-length = 100
target-version = ['py310']
include = '\\.pyi?$'
exclude = '''
/(
    \\.git
  | \\.venv
  | venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 100
skip_glob = [".venv", "venv"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
disallow_incomplete_defs = false
ignore_missing_imports = true
"""

CONFTEST_TEMPLATE = """\"\"\"
Pytest config for {name}.

Adds the local src/ to sys.path so imports work without installing.
\"\"\"

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
"""

TEST_TEMPLATE = """\"\"\"
Unit tests for {class_name} (Production)
\"\"\"

import pytest

from {name}.core import {class_name}
from {name}.models import AnalysisResult, AuditReport


@pytest.fixture
def modulo():
    \"\"\"Fixture para crear instancia de {class_name}\"\"\"
    return {class_name}()


class TestInitialization:
    \"\"\"Tests para inicializacion\"\"\"

    def test_init_default(self, modulo):
        \"\"\"Test inicializacion con valores por defecto\"\"\"
        assert modulo.name == "{class_name}"
        assert modulo.mission == "{mission}"
        assert modulo.role == "{role_code}"

    def test_init_with_config(self):
        \"\"\"Test inicializacion con configuracion\"\"\"
        config = {{"severity_threshold": "high"}}
        modulo = {class_name}(config=config)
        assert modulo.severity_threshold == "high"


class TestAudit:
    \"\"\"Tests para auditoria\"\"\"

    def test_audit(self, modulo):
        \"\"\"Test auditoria basica\"\"\"
        sample = {sample_data}
        report = modulo.{audit_method}(sample)
        assert isinstance(report, AuditReport)
        assert report.total_checks > 0


class TestAnalyze:
    \"\"\"Tests para funcionalidad de analisis\"\"\"

    def test_analyze(self, modulo):
        \"\"\"Test analyze con datos\"\"\"
        sample = {sample_data}
        result = modulo.analyze({analyze_arg}=sample)
        assert isinstance(result, AnalysisResult)
        assert result.status in ["success", "warning", "error"]


class TestValidation:
    \"\"\"Tests para validacion\"\"\"

    def test_validate_none(self, modulo):
        \"\"\"Test validacion con None\"\"\"
        assert modulo.validate(None) is False

    def test_validate_dict(self, modulo):
        \"\"\"Test validacion con diccionario valido\"\"\"
        assert modulo.validate({{"key": "value"}}) is True


class TestInfo:
    \"\"\"Tests para informacion del módulo\"\"\"

    def test_get_info_returns_dict(self, modulo):
        \"\"\"Test que get_info() retorna diccionario\"\"\"
        info = modulo.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "{class_name}"
        assert info["status"] == "Production"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
"""

INSTALL_TEMPLATE = """# Guia de Instalacion - {name}

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalacion desde PyPI

```bash
pip install {name}
```

## Instalacion desde Codigo Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/{name}
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
pip install -e ".[dev]"
```

## Verificacion de Instalacion

```python
from {name}.core import {class_name}

modulo = {class_name}()
print(modulo.get_info())
```

---

Ver tambien: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
"""

USAGE_TEMPLATE = """# Guia de Uso - {name}

## Tutorial Paso a Paso

Este tutorial muestra como usar **{class_name}** para {audit_label}.

### 1) Instalacion rapida

```bash
pip install -e .
```

### 2) Importacion e inicializacion

```python
from {name}.core import {class_name}

modulo = {class_name}()
```

### 3) Preparar los datos de entrada

```python
{analyze_arg} = {sample_data}
```

### 4) Validar los datos (opcional)

```python
if not modulo.validate({analyze_arg}):
    raise ValueError("Datos invalidos")
```

### 5) Ejecutar el analisis

```python
result = modulo.analyze({analyze_arg}={analyze_arg})
print(result.status)
print(result.message)
```

---

Ver tambien: [ARCHITECTURE.md](ARCHITECTURE.md), [API.md](API.md)
"""

API_TEMPLATE = """# API Reference - {name}

## Class: {class_name}

### Constructor

```python
{class_name}(config: Optional[Dict[str, Any]] = None)
```

**Parametros de Configuracion:**

{config_params}

### Metodos Principales

#### `{audit_method}({analyze_arg})`

Audita {audit_label} y retorna un `AuditReport`.

#### `analyze({analyze_arg})`

Ejecuta el analisis principal y retorna un `AnalysisResult`.

#### `validate(data)`

Valida datos de entrada.

#### `get_info()`

Retorna metadata del módulo.

---

Ver tambien: [USAGE.md](USAGE.md), [ARCHITECTURE.md](ARCHITECTURE.md)
"""

ARCH_TEMPLATE = """# Arquitectura - {name}

## Vision General

{name} es un modulo de ciberseguridad implementado como parte del **Snocomm Security Suite**.

- **Mision**: {mission}
- **Rol de Seguridad**: {role_display}
- **Nivel**: Production (v3.0.0)
- **Version**: 3.0.0

## Proposito

{description}

## Estructura del Componente

### 1. Core Module (`core.py`)

La clase `{class_name}` es el punto de entrada principal.

**Responsabilidades:**
- `{audit_method}()`: Ejecuta checks principales
- `analyze()`: Orquesta la auditoria y retorna `AnalysisResult`
- `validate()`: Valida inputs
- `get_info()`: Retorna metadata del módulo

### 2. Models (`models.py`)

Define estructuras Pydantic para resultados y hallazgos.

---

Ver tambien: [README.md](../README.md), [USAGE.md](USAGE.md), [API.md](API.md)
"""

EXAMPLE_TEMPLATE = """import sys
import os

# Aseguramos que podemos importar el modulo localmente para pruebas
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from {name}.core import {class_name}


def main():
    print("🚀 Iniciando mision: {mission}")
    print("🛡️  Rol: {role_display}")
    print("-" * 50)

    print("\\n[1] Inicializando {class_name}...")
    modulo = {class_name}()

    print("[2] Preparando datos...")
    {analyze_arg} = {sample_data}

    print("[3] Ejecutando analisis de seguridad...")
    result = modulo.analyze({analyze_arg}={analyze_arg})

    print("\\n[4] Informe de Mision:")
    print("-" * 30)
    print(f"Estado: {{result.status.upper()}}")
    print(f"Mensaje: {{result.message}}")
    if result.data:
        print("\\nDatos Recolectados:")
        for key, value in result.data.items():
            print(f"  - {{key}}: {{value}}")
    print("-" * 50)
    print("🏁 Mision cumplida.")


if __name__ == "__main__":
    main()
"""

EXAMPLE_README = """# 🎓 Ejemplos de Uso: {class_name}

Bienvenido al campo de entrenamiento de **{class_name}**.

Su mision, inspirada en *"{mission}"*, es clara: **{description}**

## 📂 Contenido

- `basic_usage.py`: Script listo para ejecutar con el flujo basico.

## 🚀 Como ejecutar el ejemplo

Desde este directorio:

```bash
python basic_usage.py
```

## 🧠 ¿Que esta pasando en el codigo?

El script sigue un flujo de 4 pasos:

1. **Invocacion**: Importa e instancia `{class_name}`.
2. **Preparacion**: Define datos con controles clave.
3. **Accion**: Ejecuta `.analyze()` para auditar.
4. **Reporte**: Muestra el resultado estructurado.

## 💡 Tips Pro

- Revisa `USAGE.md` para configuraciones avanzadas.
- Integra estas revisiones en auditorias periodicas.
"""


def write_if_missing(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    corporate_dir = root / "corporate"

    for item in MODULES:
        modulo_dir = corporate_dir / item["name"]

        write_if_missing(modulo_dir / "pyproject.toml", PYPROJECT_TEMPLATE.format(**item))
        write_if_missing(modulo_dir / "tests" / "conftest.py", CONFTEST_TEMPLATE.format(**item))
        write_if_missing(modulo_dir / "tests" / "test_core.py", TEST_TEMPLATE.format(**item))
        write_if_missing(modulo_dir / "docs" / "INSTALLATION.md", INSTALL_TEMPLATE.format(**item))
        write_if_missing(modulo_dir / "docs" / "USAGE.md", USAGE_TEMPLATE.format(**item))
        api_params = dict(item)
        api_params["config_params"] = "\n".join(item["config_params"])
        write_if_missing(
            modulo_dir / "docs" / "API.md",
            API_TEMPLATE.format(**api_params),
        )
        write_if_missing(modulo_dir / "docs" / "ARCHITECTURE.md", ARCH_TEMPLATE.format(**item))
        write_if_missing(modulo_dir / "examples" / "basic_usage.py", EXAMPLE_TEMPLATE.format(**item))
        write_if_missing(modulo_dir / "examples" / "README.md", EXAMPLE_README.format(**item))


if __name__ == "__main__":
    main()

