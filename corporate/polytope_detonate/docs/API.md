# API Reference - polytope_detonate

## Class: PolytopeDetonate

### Constructor

```python
PolytopeDetonate(config: Optional[Dict[str, Any]] = None)
```

**Parámetros de Configuración:**

- `severity_threshold`: Configura severity_threshold (Default: `"medium"`)

### Métodos Principales

#### `detonate_sample(sample_data)`

Ejecuta el método especializado del producto.

#### `analyze(sample_data)`

Ejecuta el análisis principal del módulo.

#### `validate(data)`

Valida datos de entrada.

#### `get_info()`

Obtener información del módulo.



## Modelos de Datos

### ModuleConfig

Configuration model for polytope_detonate

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
