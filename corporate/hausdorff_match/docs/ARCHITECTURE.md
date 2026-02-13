# Arquitectura - hausdorff_match

## Visión General

hausdorff_match es un módulo de ciberseguridad implementado como parte del **Snocomm Security Suite**.

- **Misión**: My Last Boy
- **Rol de Seguridad**: signature-matcher
- **Nivel**: Production (v3.0.0)
- **Versión**: 3.0.0

## Propósito

Correlaciona firmas y variantes para acelerar clasificacion de amenazas.

## Estructura del Componente

### 1. Core Module (`core.py`)

La clase `HausdorffMatch` es el punto de entrada principal. Implementa la lógica de negocio y orquesta las operaciones de seguridad.

**Responsabilidades:**
- `match_signatures()`: Ejecuta el método especializado del producto
- `analyze()`: Ejecuta el análisis principal del módulo
- `validate()`: Valida datos de entrada
- `get_info()`: Obtener información del módulo


### 2. Models (`models.py`)

Define la estructura de datos utilizando **Pydantic v2**, asegurando validación estricta y serialización segura.

**Modelos Principales:**
- `ModuleConfig`: Configuration model for hausdorff_match
- `DetectionFinding`: Detection finding
- `DetectionReport`: Result of specialized threat analysis
- `AnalysisResult`: Result model for analysis operations
- `ModuleInfo`: Information model for module metadata


### 3. Utils (`utils.py`)

Proporciona utilidades auxiliares como configuración de logging y helpers comunes.

## Configuración y Personalización

El módulo se configura mediante un diccionario inmutable (`frozen=True` en Pydantic) pasado al inicializador.

```python
config = {
    "severity_threshold": "medium",  # Configura severity_threshold
}
```

## Flujo de Trabajo Típico

1. **Inicialización**: Se carga la configuración y se validan las dependencias.
2. **Validación**: `validate()` verifica que los inputs cumplan los requisitos mínimos.
3. **Ejecución**: `analyze()` (u otros métodos específicos) procesa los datos aplicando la lógica de seguridad.
4. **Resultado**: Se retorna un objeto `AnalysisResult` estandarizado con estado, mensaje y datos.

## Estándares de Seguridad (2025-2026)

- **Validación de Tipos**: Uso extensivo de Type Hints y Pydantic.
- **Manejo de Errores Seguro**: Los errores se capturan y retornan estructurados, evitando crash no controlados.
- **Configuración Inmutable**: Previene modificaciones accidentales en tiempo de ejecución.

## Extensibilidad

Para agregar nuevas funcionalidades:
1. Definir nuevos modelos en `models.py`.
2. Implementar la lógica en `core.py`.
3. Agregar pruebas unitarias en `tests/test_core.py`.

---

Ver también: [README.md](../README.md), [USAGE.md](USAGE.md), [API.md](API.md)
