# API Reference - affine_replica

## Class: AffineReplica

### Constructor

```python
AffineReplica(config: Optional[Dict[str, Any]] = None)
```

**Parámetros de Configuración:**

- `severity_threshold`: Configura severity_threshold (Default: `"medium"`)

### Métodos Principales

#### `emulate_behavior(execution_data)`

Ejecuta el método especializado del producto.

#### `analyze(execution_data)`

Ejecuta el análisis principal del módulo.

#### `validate(data)`

Valida datos de entrada.

#### `get_info()`

Obtener información del módulo.



## Modelos de Datos

### ModuleConfig

Configuration model for affine_replica

**Campos:**
- `name`
- `severity_threshold`
- `confidence_threshold`
- `enable_enrichment`
- `debug`

### DetectionFinding

Detection finding

**Campos:**
- `indicator`
- `category`
- `severity`
- `confidence`
- `recommendation`

### DetectionReport

Result of specialized threat analysis

**Campos:**
- `total_checks`
- `alerts_count`
- `findings`
- `summary`

### AnalysisResult

Result model for analysis operations

**Campos:**
- `status`
- `message`
- `data`
- `errors`

### ModuleInfo

Information model for module metadata

**Campos:**
- `name`
- `mission`
- `role`
- `status`
- `severity_threshold`
- `confidence_threshold`
- `version`



---

Ver también: [USAGE.md](USAGE.md), [ARCHITECTURE.md](ARCHITECTURE.md)
