# Arquitectura - forensimon

## Visión General

forensimon es un módulo de ciberseguridad implementado como parte del **DIGIMON CYBERSECURITY SUITE**.

**Misión**: The New South  
**Rol de Seguridad**: forensics-analyzer

## Componentes Principales

### 1. Core Module (`core.py`)

Contiene la clase principal `Forensimon` que implementa la lógica central.

- `__init__()` - Inicialización
- `analyze()` - Análisis principal
- `validate()` - Validación de datos
- `get_info()` - Metadata del Digimon

### 2. Models (`models.py`)

Define tipos y esquemas usando Pydantic:
- `DigimonConfig` - Configuración
- `AnalysisResult` - Resultados
- `DigimonInfo` - Información

### 3. Utils (`utils.py`)

- `setup_logging()` - Configurar logging
- `format_result()` - Formatear resultados
- `validate_input()` - Validar tipos

---

Ver también: [README.md](../README.md), [USAGE.md](USAGE.md)
