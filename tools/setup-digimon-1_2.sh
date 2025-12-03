#!/bin/bash

################################################################################
# DIGIMON CYBERSECURITY SUITE - Generador Automático de Estructura
# Versión macOS Sequoia (BSD sed compatible)
# Uso: ./setup_digimon.sh --name thirstmon --mission "Good, Honest Snake Oil" ...
################################################################################

set -e

# Colors para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables
DIGIMON_NAME=""
MISSION=""
ROLE=""
DESCRIPTION=""
LANGUAGE="python"
VERSION="0.1.0"
AUTHOR="Anonymous"
LICENSE="MIT"
YEAR=$(date +%Y)

# Funciones
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

show_help() {
    cat << EOF
DIGIMON CYBERSECURITY SUITE - Setup Tool

Uso: ./setup_digimon.sh [opciones]

Opciones:
  --name NAME             Nombre del Digimon (requerido)
  --mission MISSION       Misión RDR2 inspiradora (requerido)
  --role ROLE             Rol de ciberseguridad (requerido)
  --description DESC      Descripción detallada (requerido)
  --language LANG         Lenguaje (default: python)
  --version VERSION       Versión inicial (default: 0.1.0)
  --author AUTHOR         Autor (default: Anonymous)
  --license LICENSE       Licencia MIT|Apache2.0 (default: MIT)
  --base-dir DIR          Directorio base (default: ./digimons)
  --help                  Muestra esta ayuda

Ejemplo:
  ./setup_digimon.sh \\
    --name thirstmon \\
    --mission "Good, Honest Snake Oil" \\
    --role "threat-filter" \\
    --description "Filtra indicadores de compromiso maliciosos" \\
    --author "Tu Nombre"

EOF
}

# Parser de argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        --name) DIGIMON_NAME="$2"; shift 2 ;;
        --mission) MISSION="$2"; shift 2 ;;
        --role) ROLE="$2"; shift 2 ;;
        --description) DESCRIPTION="$2"; shift 2 ;;
        --language) LANGUAGE="$2"; shift 2 ;;
        --version) VERSION="$2"; shift 2 ;;
        --author) AUTHOR="$2"; shift 2 ;;
        --license) LICENSE="$2"; shift 2 ;;
        --base-dir) BASE_DIR="$2"; shift 2 ;;
        --help) show_help; exit 0 ;;
        *) print_error "Opción desconocida: $1"; show_help; exit 1 ;;
    esac
done

# Validaciones
if [ -z "$DIGIMON_NAME" ] || [ -z "$MISSION" ] || [ -z "$ROLE" ] || [ -z "$DESCRIPTION" ]; then
    print_error "Faltan parámetros requeridos"
    show_help
    exit 1
fi

BASE_DIR="${BASE_DIR:-.}/digimons"
DIGIMON_PATH="$BASE_DIR/$DIGIMON_NAME"

# Verificar si ya existe
if [ -d "$DIGIMON_PATH" ]; then
    print_error "El Digimon '$DIGIMON_NAME' ya existe en $DIGIMON_PATH"
    exit 1
fi

print_header "Generando Digimon: $DIGIMON_NAME"
print_info "Misión: $MISSION"
print_info "Rol: $ROLE"

# Crear estructura de directorios
print_info "Creando estructura de directorios..."
mkdir -p "$DIGIMON_PATH"/{src/$DIGIMON_NAME,tests,docs,examples,.github/workflows}
print_success "Directorios creados"

# ============================================================================
# FUNCIÓN PARA REEMPLAZAR VARIABLES (macOS compatible)
# ============================================================================

replace_in_file() {
    local file="$1"
    local old="$2"
    local new="$3"
    
    # Escapar caracteres especiales en 'new'
    new=$(echo "$new" | sed 's/[&/\]/\\&/g')
    
    # macOS BSD sed requiere '' después de -i
    sed -i '' "s|$old|$new|g" "$file"
}

# ============================================================================
# 1. README.md
# ============================================================================

cat > "$DIGIMON_PATH/README.md" << 'EOF'
# 🎮 {{DIGIMON_NAME}} - {{ROLE_DISPLAY}}

**Misión RDR2**: {{MISSION}}  
**Rol de Ciberseguridad**: {{ROLE}}  
**Estado**: Rookie (v{{VERSION}})  
**Mantenedor**: {{AUTHOR}}  
**Licencia**: {{LICENSE}}

## 🎯 Propósito

{{DESCRIPTION}}

### Contexto Temático

En el universo de **DIGIMON CYBERSECURITY SUITE**, cada Digimon representa una especialidad de seguridad. {{DIGIMON_NAME}} encarna los principios de la misión "{{MISSION}}" de Red Dead Redemption 2, aplicados al dominio cibernético.

## 🚀 Inicio Rápido

### Instalación

```bash
# Desde el repositorio principal
cd digimons/{{DIGIMON_NAME}}
pip install -e .

# O instalación directa
pip install {{DIGIMON_NAME}}
```

### Uso Básico

```python
from {{DIGIMON_NAME}} import {{DIGIMON_CAMEL}}

# Crear instancia
digimon = {{DIGIMON_CAMEL}}()

# Usar funcionalidad principal
result = digimon.analyze()
print(result)
```

## 📚 Documentación

- [Arquitectura](docs/ARCHITECTURE.md) - Diseño técnico interno
- [Guía de Uso](docs/USAGE.md) - Ejemplos y patrones
- [API Reference](docs/API.md) - Documentación de funciones
- [Instalación](docs/INSTALLATION.md) - Pasos de setup

## 🔄 Línea Evolutiva (Versioning)

El desarrollo de {{DIGIMON_NAME}} sigue la línea evolutiva de los Digimons:

| Fase | Versión | Características | Timeline |
|------|---------|-----------------|----------|
| 🔴 Rookie | 0.1.x | MVP básico, funcionalidad core | Actual |
| 🟠 Champion | 1.0.x | Integración con APIs, mejoras | Q2 2025 |
| 🟡 Ultimate | 2.0.x | Procesamiento avanzado, optimizaciones | Q3 2025 |
| 🟢 Mega | 3.0.x | Características AI/ML, distribución | Q4 2025 |

## 🛠️ Desarrollo Local

### Setup

```bash
# Clonar y navegar
cd digimons/{{DIGIMON_NAME}}

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar en modo desarrollo
pip install -e ".[dev]"
```

### Testing

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov={{DIGIMON_NAME}}

# Tests específicos
pytest tests/test_core.py -v
```

### Linting

```bash
black src/ tests/
flake8 src/ tests/
mypy src/
```

## 📁 Estructura del Proyecto

```
{{DIGIMON_NAME}}/
├── src/{{DIGIMON_NAME}}/
│   ├── __init__.py
│   ├── core.py              # Lógica principal
│   ├── models.py            # Modelos y tipos
│   ├── utils.py             # Utilidades
│   └── cli.py               # Interfaz CLI (opcional)
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   └── test_integration.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── USAGE.md
│   └── INSTALLATION.md
├── examples/
│   ├── basic_usage.py
│   └── demo.sh
├── pyproject.toml           # Configuración de proyecto
├── requirements.txt         # Dependencias
├── CHANGELOG.md             # Historial de versiones
├── LICENSE                  # Licencia
└── README.md                # Este archivo
```

## 🤝 Contribuir

Este proyecto es parte de [DIGIMON CYBERSECURITY SUITE](https://github.com/yourusername/digimon-sec-suite).

Por favor, consulta [CONTRIBUTING.md](../../CONTRIBUTING.md) para:
- Pautas de código
- Proceso de pull requests
- Líneas de evolución
- Estándares de documentación

## 📄 Licencia

{{LICENSE}} - Ver archivo [LICENSE](LICENSE)

## 🔗 Enlaces Útiles

- [DIGIMON CYBERSECURITY SUITE](https://github.com/yourusername/digimon-sec-suite)
- [Documentación Global](../../docs/)
- [Catálogo de Digimons](../../digimons/README_DIGIMONS.md)
- [Issues & Discussions](https://github.com/yourusername/digimon-sec-suite/issues)

---

**Última actualización**: {{YEAR}}  
**Status**: 🔴 Rookie Era (v{{VERSION}})
EOF

# Reemplazar variables en README
replace_in_file "$DIGIMON_PATH/README.md" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/README.md" "{{DIGIMON_CAMEL}}" "$(echo $DIGIMON_NAME | sed 's/^./\U&/' | sed 's/-\(.\)/\U\1/g')"
replace_in_file "$DIGIMON_PATH/README.md" "{{MISSION}}" "$MISSION"
replace_in_file "$DIGIMON_PATH/README.md" "{{ROLE}}" "$ROLE"
replace_in_file "$DIGIMON_PATH/README.md" "{{ROLE_DISPLAY}}" "$(echo $ROLE | sed 's/-/ /g' | sed 's/\b\(.\)/\U\1/g')"
replace_in_file "$DIGIMON_PATH/README.md" "{{DESCRIPTION}}" "$DESCRIPTION"
replace_in_file "$DIGIMON_PATH/README.md" "{{VERSION}}" "$VERSION"
replace_in_file "$DIGIMON_PATH/README.md" "{{AUTHOR}}" "$AUTHOR"
replace_in_file "$DIGIMON_PATH/README.md" "{{LICENSE}}" "$LICENSE"
replace_in_file "$DIGIMON_PATH/README.md" "{{YEAR}}" "$YEAR"

print_success "README.md generado"

# ============================================================================
# 2. pyproject.toml
# ============================================================================

cat > "$DIGIMON_PATH/pyproject.toml" << 'EOF'
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[project]
name = "{{DIGIMON_NAME}}"
version = "{{VERSION}}"
description = "{{DESCRIPTION}}"
readme = "README.md"
license = {text = "{{LICENSE}}"}
authors = [{name = "{{AUTHOR}}", email = "dev@example.com"}]
requires-python = ">=3.10"
keywords = ["cybersecurity", "digimon", "{{ROLE}}", "{{DIGIMON_NAME}}"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Security",
    "License :: OSI Approved :: {{LICENSE_CLASSIFIER}} License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    "requests>=2.28.0",
    "click>=8.0.0",
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
Homepage = "https://github.com/yourusername/digimon-sec-suite"
Documentation = "https://digimon-sec-suite.readthedocs.io"
Repository = "https://github.com/yourusername/digimon-sec-suite/tree/main/digimons/{{DIGIMON_NAME}}"
Issues = "https://github.com/yourusername/digimon-sec-suite/issues"

[tool.poetry]
packages = [{include = "{{DIGIMON_NAME}}", from = "src"}]

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
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
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
EOF

# Reemplazar variables en pyproject.toml
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{VERSION}}" "$VERSION"
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{DESCRIPTION}}" "$DESCRIPTION"
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{AUTHOR}}" "$AUTHOR"
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{LICENSE}}" "$LICENSE"
LICENSE_CLASSIFIER=$([ "$LICENSE" = "MIT" ] && echo "MIT" || echo "Apache Software License")
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{LICENSE_CLASSIFIER}}" "$LICENSE_CLASSIFIER"
replace_in_file "$DIGIMON_PATH/pyproject.toml" "{{ROLE}}" "$ROLE"

print_success "pyproject.toml generado"

# ============================================================================
# 3. requirements.txt
# ============================================================================

cat > "$DIGIMON_PATH/requirements.txt" << 'EOF'
# Core Dependencies
requests>=2.28.0
click>=8.0.0
pydantic>=2.0.0
aiohttp>=3.8.0
python-dotenv>=1.0.0

# Dev Dependencies (opcional)
# pytest>=7.4.0
# pytest-cov>=4.1.0
# black>=23.0.0
# flake8>=6.0.0
# mypy>=1.4.0
EOF

print_success "requirements.txt generado"

# ============================================================================
# 4. src/__init__.py
# ============================================================================

cat > "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" << 'EOF'
"""
{{DIGIMON_NAME}} - Cybersecurity Module
Part of DIGIMON CYBERSECURITY SUITE

Misión: {{MISSION}}
Rol: {{ROLE}}
"""

__version__ = "{{VERSION}}"
__author__ = "{{AUTHOR}}"
__license__ = "{{LICENSE}}"

from .core import {{DIGIMON_CAMEL}}

__all__ = ["{{DIGIMON_CAMEL}}", "__version__"]
EOF

DIGIMON_CAMEL=$(echo $DIGIMON_NAME | sed 's/^./\U&/' | sed 's/-\(.\)/\U\1/g')

replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{MISSION}}" "$MISSION"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{ROLE}}" "$ROLE"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{VERSION}}" "$VERSION"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{AUTHOR}}" "$AUTHOR"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" "{{LICENSE}}" "$LICENSE"

print_success "src/__init__.py generado"

# ============================================================================
# 5. src/core.py
# ============================================================================

cat > "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" << 'EOF'
"""
Core functionality for {{DIGIMON_NAME}}

This module contains the main logic and class definitions for {{DIGIMON_NAME}}.
Misión: {{MISSION}}
Rol: {{ROLE}}
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class {{DIGIMON_CAMEL}}:
    """
    {{DIGIMON_CAMEL}} - Cybersecurity Module
    
    Descripción:
        {{DESCRIPTION}}
    
    Attributes:
        name: Nombre del Digimon
        mission: Misión RDR2 inspiradora
        role: Rol en ciberseguridad
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializar {{DIGIMON_CAMEL}}
        
        Args:
            config: Diccionario de configuración opcional
        """
        self.name = "{{DIGIMON_NAME}}"
        self.mission = "{{MISSION}}"
        self.role = "{{ROLE}}"
        self.config = config or {}
        logger.info(f"Initialized {self.name} - {self.role}")
    
    def analyze(self) -> Dict[str, Any]:
        """
        Ejecutar análisis principal
        
        Returns:
            Diccionario con resultados del análisis
        """
        logger.debug(f"Running analysis in {self.name}")
        
        result = {
            "status": "success",
            "message": f"{self.name} analysis completed",
            "data": {}
        }
        
        return result
    
    def validate(self, data: Any) -> bool:
        """
        Validar datos de entrada
        
        Args:
            data: Datos a validar
        
        Returns:
            True si válido, False en caso contrario
        """
        if data is None:
            return False
        
        return True
    
    def get_info(self) -> Dict[str, str]:
        """
        Obtener información del Digimon
        
        Returns:
            Diccionario con información
        """
        return {
            "name": self.name,
            "mission": self.mission,
            "role": self.role,
            "status": "Rookie"
        }


# Alias para retrocompatibilidad
Digimon = {{DIGIMON_CAMEL}}
EOF

replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" "{{MISSION}}" "$MISSION"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" "{{ROLE}}" "$ROLE"
replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" "{{DESCRIPTION}}" "$DESCRIPTION"

print_success "src/core.py generado"

# ============================================================================
# 6. src/models.py
# ============================================================================

cat > "$DIGIMON_PATH/src/$DIGIMON_NAME/models.py" << 'EOF'
"""
Data models for {{DIGIMON_NAME}}

Define Pydantic models for type validation and documentation.
"""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class DigimonConfig(BaseModel):
    """Configuration model for {{DIGIMON_NAME}}"""
    
    name: str = Field(default="{{DIGIMON_NAME}}", description="Digimon name")
    debug: bool = Field(default=False, description="Enable debug mode")
    timeout: int = Field(default=30, ge=1, description="Request timeout in seconds")
    
    class Config:
        """Pydantic config"""
        frozen = True


class AnalysisResult(BaseModel):
    """Result model for analysis operations"""
    
    status: str = Field(description="Status of the analysis")
    message: str = Field(description="Descriptive message")
    data: Dict[str, Any] = Field(default_factory=dict, description="Result data")
    errors: Optional[list] = Field(default=None, description="List of errors if any")


class DigimonInfo(BaseModel):
    """Information model for Digimon metadata"""
    
    name: str
    mission: str
    role: str
    status: str
    version: str = "0.1.0"
EOF

replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/models.py" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"

print_success "src/models.py generado"

# ============================================================================
# 7. src/utils.py
# ============================================================================

cat > "$DIGIMON_PATH/src/$DIGIMON_NAME/utils.py" << 'EOF'
"""
Utility functions for {{DIGIMON_NAME}}
"""

import logging
from typing import Any, Dict


logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """
    Configure logging for {{DIGIMON_NAME}}
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def format_result(status: str, message: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Format standard result dictionary
    
    Args:
        status: Result status
        message: Descriptive message
        data: Optional data payload
    
    Returns:
        Formatted result dictionary
    """
    return {
        "status": status,
        "message": message,
        "data": data or {}
    }


def validate_input(value: Any, expected_type: type) -> bool:
    """
    Validate input against expected type
    
    Args:
        value: Value to validate
        expected_type: Expected Python type
    
    Returns:
        True if valid, False otherwise
    """
    try:
        return isinstance(value, expected_type)
    except Exception as e:
        logger.error(f"Validation error: {e}")
        return False
EOF

replace_in_file "$DIGIMON_PATH/src/$DIGIMON_NAME/utils.py" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"

print_success "src/utils.py generado"

# ============================================================================
# 8. tests/__init__.py y test_core.py
# ============================================================================

touch "$DIGIMON_PATH/tests/__init__.py"

cat > "$DIGIMON_PATH/tests/test_core.py" << 'EOF'
"""
Unit tests for {{DIGIMON_NAME}} core module
"""

import pytest
from {{DIGIMON_NAME}}.core import {{DIGIMON_CAMEL}}


@pytest.fixture
def digimon():
    """Fixture para crear instancia de {{DIGIMON_CAMEL}}"""
    return {{DIGIMON_CAMEL}}()


class TestInitialization:
    """Tests para inicialización"""
    
    def test_init_default(self):
        """Test inicialización con valores por defecto"""
        digimon = {{DIGIMON_CAMEL}}()
        assert digimon.name == "{{DIGIMON_NAME}}"
        assert digimon.mission == "{{MISSION}}"
        assert digimon.role == "{{ROLE}}"
    
    def test_init_with_config(self):
        """Test inicialización con configuración"""
        config = {"debug": True}
        digimon = {{DIGIMON_CAMEL}}(config=config)
        assert digimon.config == config


class TestAnalysis:
    """Tests para funcionalidad de análisis"""
    
    def test_analyze_returns_dict(self, digimon):
        """Test que analyze() retorna diccionario"""
        result = digimon.analyze()
        assert isinstance(result, dict)
        assert "status" in result
        assert "message" in result
    
    def test_analyze_success_status(self, digimon):
        """Test que analyze() retorna status success"""
        result = digimon.analyze()
        assert result["status"] == "success"


class TestValidation:
    """Tests para validación"""
    
    def test_validate_none(self, digimon):
        """Test validación con None"""
        assert digimon.validate(None) is False
    
    def test_validate_valid_data(self, digimon):
        """Test validación con datos válidos"""
        assert digimon.validate({"key": "value"}) is True


class TestInfo:
    """Tests para información del Digimon"""
    
    def test_get_info_returns_dict(self, digimon):
        """Test que get_info() retorna diccionario"""
        info = digimon.get_info()
        assert isinstance(info, dict)
        assert info["name"] == "{{DIGIMON_NAME}}"
        assert info["status"] == "Rookie"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
EOF

replace_in_file "$DIGIMON_PATH/tests/test_core.py" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/tests/test_core.py" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"
replace_in_file "$DIGIMON_PATH/tests/test_core.py" "{{MISSION}}" "$MISSION"
replace_in_file "$DIGIMON_PATH/tests/test_core.py" "{{ROLE}}" "$ROLE"

print_success "tests/test_core.py generado"

# ============================================================================
# 9. Documentación (simplificada para espacio)
# ============================================================================

cat > "$DIGIMON_PATH/docs/ARCHITECTURE.md" << 'EOF'
# Arquitectura - {{DIGIMON_NAME}}

## Visión General

{{DIGIMON_NAME}} es un módulo de ciberseguridad implementado como parte del **DIGIMON CYBERSECURITY SUITE**.

**Misión**: {{MISSION}}  
**Rol de Seguridad**: {{ROLE}}

## Componentes Principales

### 1. Core Module (`core.py`)

Contiene la clase principal `{{DIGIMON_CAMEL}}` que implementa la lógica central.

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
EOF

replace_in_file "$DIGIMON_PATH/docs/ARCHITECTURE.md" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/docs/ARCHITECTURE.md" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"
replace_in_file "$DIGIMON_PATH/docs/ARCHITECTURE.md" "{{MISSION}}" "$MISSION"
replace_in_file "$DIGIMON_PATH/docs/ARCHITECTURE.md" "{{ROLE}}" "$ROLE"

# USAGE.md
cat > "$DIGIMON_PATH/docs/USAGE.md" << 'EOF'
# Guía de Uso - {{DIGIMON_NAME}}

## Inicio Rápido

### Instalación

```bash
pip install -e .
```

### Uso Básico

```python
from {{DIGIMON_NAME}}.core import {{DIGIMON_CAMEL}}

digimon = {{DIGIMON_CAMEL}}()
result = digimon.analyze()
print(result)
```

---

Ver también: [ARCHITECTURE.md](ARCHITECTURE.md), [API.md](API.md)
EOF

replace_in_file "$DIGIMON_PATH/docs/USAGE.md" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/docs/USAGE.md" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"

# API.md
cat > "$DIGIMON_PATH/docs/API.md" << 'EOF'
# API Reference - {{DIGIMON_NAME}}

## Class: {{DIGIMON_CAMEL}}

### Constructor

```python
{{DIGIMON_CAMEL}}(config: Optional[Dict[str, Any]] = None)
```

### Methods

- `analyze()` - Execute main analysis
- `validate(data)` - Validate input data
- `get_info()` - Get Digimon metadata

---

Ver también: [USAGE.md](USAGE.md), [ARCHITECTURE.md](ARCHITECTURE.md)
EOF

replace_in_file "$DIGIMON_PATH/docs/API.md" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/docs/API.md" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"

# INSTALLATION.md
cat > "$DIGIMON_PATH/docs/INSTALLATION.md" << 'EOF'
# Guía de Instalación - {{DIGIMON_NAME}}

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install {{DIGIMON_NAME}}
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/yourusername/digimon-sec-suite.git
cd digimon-sec-suite/digimons/{{DIGIMON_NAME}}
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

---

Ver también: [USAGE.md](USAGE.md), [README.md](../README.md)
EOF

replace_in_file "$DIGIMON_PATH/docs/INSTALLATION.md" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"

print_success "Documentación generada"

# ============================================================================
# 10. examples/
# ============================================================================

cat > "$DIGIMON_PATH/examples/basic_usage.py" << 'EOF'
"""
Basic usage example for {{DIGIMON_NAME}}
"""

import sys
sys.path.insert(0, '../src')

from {{DIGIMON_NAME}}.core import {{DIGIMON_CAMEL}}
from {{DIGIMON_NAME}}.utils import setup_logging


def main():
    setup_logging(level="INFO")
    digimon = {{DIGIMON_CAMEL}}()
    
    print("=== Digimon Info ===")
    info = digimon.get_info()
    for key, value in info.items():
        print(f"{key}: {value}")
    
    print("\n=== Validation Test ===")
    is_valid = digimon.validate({"test": "data"})
    print(f"Data valid: {is_valid}")
    
    print("\n=== Running Analysis ===")
    result = digimon.analyze()
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
EOF

replace_in_file "$DIGIMON_PATH/examples/basic_usage.py" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/examples/basic_usage.py" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"

# demo.sh
cat > "$DIGIMON_PATH/examples/demo.sh" << 'EOF'
#!/bin/bash

echo "=== {{DIGIMON_NAME}} Demo ==="
echo ""

cd "$(dirname "$0")/.."

echo "1. Installing dependencies..."
pip install -e . -q

echo ""
echo "2. Running basic usage example..."
python examples/basic_usage.py

echo ""
echo "3. Running tests..."
pytest tests/ -q

echo ""
echo "✓ Demo complete!"
EOF

chmod +x "$DIGIMON_PATH/examples/demo.sh"
replace_in_file "$DIGIMON_PATH/examples/demo.sh" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"

print_success "Ejemplos generados"

# ============================================================================
# 11. .github/workflows/
# ============================================================================

cat > "$DIGIMON_PATH/.github/workflows/test-$DIGIMON_NAME.yml" << 'EOF'
name: Test {{DIGIMON_NAME}}

on:
  push:
    branches: [main, develop]
    paths:
      - 'digimons/{{DIGIMON_NAME}}/**'
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
    
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: cd digimons/{{DIGIMON_NAME}} && pip install -e ".[dev]"
      - run: cd digimons/{{DIGIMON_NAME}} && pytest tests/ -v --cov
EOF

replace_in_file "$DIGIMON_PATH/.github/workflows/test-$DIGIMON_NAME.yml" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"

print_success "GitHub Actions workflow generado"

# ============================================================================
# 12. CHANGELOG.md
# ============================================================================

cat > "$DIGIMON_PATH/CHANGELOG.md" << 'EOF'
# Changelog - {{DIGIMON_NAME}}

## [0.1.0] - {{YEAR}}-01-15 - 🔴 Rookie Era

### Added
- Initial release
- Core {{DIGIMON_CAMEL}} class
- Basic analysis functionality
- Data validation
- Logging utilities
- Comprehensive test suite
- Full documentation

### Features
- {{DESCRIPTION}}

---

## Línea Evolutiva (Versioning)

- 🔴 Rookie (v0.1.x) - MVP básico con funcionalidad core
- 🟠 Champion (v1.0.x) - Integraciones con APIs
- 🟡 Ultimate (v2.0.x) - Procesamiento avanzado
- 🟢 Mega (v3.0.x) - Características AI/ML

---

[0.1.0]: https://github.com/yourusername/digimon-sec-suite/releases/tag/v0.1.0
EOF

replace_in_file "$DIGIMON_PATH/CHANGELOG.md" "{{DIGIMON_NAME}}" "$DIGIMON_NAME"
replace_in_file "$DIGIMON_PATH/CHANGELOG.md" "{{DIGIMON_CAMEL}}" "$DIGIMON_CAMEL"
replace_in_file "$DIGIMON_PATH/CHANGELOG.md" "{{DESCRIPTION}}" "$DESCRIPTION"
replace_in_file "$DIGIMON_PATH/CHANGELOG.md" "{{YEAR}}" "$YEAR"

print_success "CHANGELOG.md generado"

# ============================================================================
# 13. LICENSE
# ============================================================================

if [ "$LICENSE" = "MIT" ]; then
    cat > "$DIGIMON_PATH/LICENSE" << 'EOF'
MIT License

Copyright (c) 2025 {{AUTHOR}}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
EOF
else
    cat > "$DIGIMON_PATH/LICENSE" << 'EOF'
Apache License Version 2.0, January 2004

(Ver https://www.apache.org/licenses/LICENSE-2.0.txt para el texto completo)
EOF
fi

replace_in_file "$DIGIMON_PATH/LICENSE" "{{AUTHOR}}" "$AUTHOR"

print_success "LICENSE generado"

# ============================================================================
# 14. .gitignore
# ============================================================================

cat > "$DIGIMON_PATH/.gitignore" << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/
.env
.venv
venv/
.pytest_cache/
.coverage
htmlcov/
.idea/
*.swp
.DS_Store
EOF

print_success ".gitignore generado"

# ============================================================================
# Summary
# ============================================================================

print_header "✅ DIGIMON GENERADO EXITOSAMENTE"

echo ""
echo "Información del Digimon:"
echo "  Nombre: $DIGIMON_NAME"
echo "  Misión: $MISSION"
echo "  Rol: $ROLE"
echo "  Versión: $VERSION"
echo "  Ubicación: $DIGIMON_PATH"

echo ""
echo "Estructura creada:"
echo "  ✓ Código fuente (src/)"
echo "  ✓ Tests unitarios (tests/)"
echo "  ✓ Documentación completa (docs/)"
echo "  ✓ Ejemplos de uso (examples/)"
echo "  ✓ GitHub Actions CI/CD (.github/workflows/)"
echo "  ✓ Configuración de proyecto (pyproject.toml, requirements.txt)"
echo "  ✓ Licencia ($LICENSE)"

echo ""
echo "Próximos pasos:"
echo "  1. cd $DIGIMON_PATH"
echo "  2. python -m venv venv"
echo "  3. source venv/bin/activate  # En Windows: venv\\Scripts\\activate"
echo "  4. pip install -e \".[dev]\""
echo "  5. pytest                    # Ejecutar tests"
echo "  6. python examples/basic_usage.py  # Ver demo"

echo ""
print_success "¡Listo para desarrollar!"
