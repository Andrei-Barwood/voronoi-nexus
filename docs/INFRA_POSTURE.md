# Snocomm — Revisión de postura para infraestructura interna

Guía para equipos de desarrollo e infraestructura que necesitan evaluar la **postura de ciberseguridad** de hardware, red, acceso y plataformas internas sin instalar Python ni clonar el monorepo.

---

## Qué obtienes

Un ejecutable **`snocomm`** que incluye:

- Los **77 módulos** del catálogo Snocomm
- Comando **`posture`** con **17 controles** orientados a infraestructura interna
- Reporte con score global, categorías y acciones prioritarias

---

## Inicio rápido (sin Python)

1. Descarga el binario para tu plataforma desde [GitHub Releases](https://github.com/Andrei-Barwood/voronoi-nexus/releases):

| Plataforma | Archivo |
|------------|---------|
| Linux x86_64 | `snocomm-linux-x86_64` |
| macOS Apple Silicon | `snocomm-darwin-arm64` |
| Windows x86_64 | `snocomm-windows-x86_64.exe` |

2. En terminal:

```bash
chmod +x snocomm-linux-x86_64    # Linux
./snocomm-linux-x86_64 --version
./snocomm-linux-x86_64 posture
./snocomm-linux-x86_64 posture --json --output infra-posture-report.json
```

macOS:

```bash
chmod +x snocomm-darwin-arm64
./snocomm-darwin-arm64 posture --output infra-posture-report.json
```

Windows:

```powershell
.\snocomm-windows-x86_64.exe posture --output infra-posture-report.json
```

---

## Comando `posture` — qué evalúa

| Categoría | Módulos | Enfoque |
|-----------|---------|---------|
| `cloud_config` | Fractal Axiom | Hardening cloud |
| `network` | Vertex Stillness, Hyperplane Guard, Geodesic Network | VPC, firewall, tráfico |
| `access` | Geodesic Identity, Lattice Permission | IAM y permisos |
| `compute` | Polytope Cluster, Simplex Container | K8s y contenedores |
| `iac` | Manifold Code | Terraform / IaC |
| `hardware` | Lattice Resource | Capacidad y uso de recursos |
| `storage` | Torus Vault, Helix Vault | Almacenamiento y bases de datos |
| `vulnerabilities` | Vertex Vuln | CVEs y exposición |
| `code` | Vertex Scan | Análisis estático |
| `governance` | Lattice Policy | Políticas |
| `visibility` | Torus Log | Logs |
| `response` | Helix Incident | Respuesta a incidentes |

### Interpretación del score

| Nivel | Score | Significado |
|-------|-------|-------------|
| `STRONG` | ≥ 85 | Postura sólida; revisar warnings menores |
| `MODERATE` | 65–84 | Gaps moderados; priorizar acciones listadas |
| `NEEDS_ATTENTION` | < 65 | Riesgo elevado; remediación urgente |

---

## Datos reales de tu infraestructura

Por defecto, los módulos corren con **datos demo**. Para alimentar controles con tu entorno interno, crea `infra-input.json`:

```json
{
  "vertex_stillness": {
    "vpc_data": {
      "flow_logs_enabled": true,
      "public_subnets": false,
      "network_acl_restrictive": true
    }
  },
  "hyperplane_guard": {
    "rules_data": {
      "default_deny": true,
      "open_ports": [443],
      "logging_enabled": true
    }
  },
  "lattice_resource": {
    "usage_data": {
      "cpu_utilization": 72,
      "memory_utilization": 68,
      "disk_utilization": 55
    }
  }
}
```

Ejecuta:

```bash
./snocomm posture --input infra-input.json --output report.json
```

---

## Otros comandos útiles

```bash
./snocomm list --domain network
./snocomm run vertex-vuln --json
./snocomm run hyperplane-guard --input firewall-rules.json
./snocomm info geodesic-identity
```

---

## Construir el ejecutable desde fuente

```bash
pip install -e ".[executable]"
python tools/build_executable.py --onefile --clean
# Salida: dist/snocomm-{linux|darwin|windows}-{arch}[.exe]
```

---

*Snocomm Security Suite — Herramienta de referencia para revisiones de postura. Complementa, no sustituye, auditorías formales ni herramientas de inventario de tu organización.*