#!/bin/bash

################################################################################
# DIGIMON CYBERSECURITY SUITE - Generador Automático (macOS Fixed v2)
# Solución: Usa Python para strings en lugar de sed incompatible
################################################################################

set -e

# Colors para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variables Defaults
DIGIMON_NAME=""
MISSION=""
ROLE=""
DESCRIPTION=""
LANGUAGE="python"
VERSION="0.1.0"
AUTHOR="Anonymous"
LICENSE="MIT"
YEAR=$(date +%Y)

# Funciones de UI
print_header() { echo -e "${BLUE}========================================${NC}\n${BLUE}$1${NC}\n${BLUE}========================================${NC}"; }
print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_info() { echo -e "${YELLOW}ℹ $1${NC}"; }

show_help() {
    cat << EOF
Uso: ./setup_digimon.sh --name [nombre] ...
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
        *) echo "Opción desconocida: $1"; exit 1 ;;
    esac
done

if [ -z "$DIGIMON_NAME" ] || [ -z "$MISSION" ] || [ -z "$ROLE" ] || [ -z "$DESCRIPTION" ]; then
    print_error "Faltan parámetros."
    exit 1
fi

BASE_DIR="${BASE_DIR:-.}/digimons"
DIGIMON_PATH="$BASE_DIR/$DIGIMON_NAME"

if [ -d "$DIGIMON_PATH" ]; then
    print_error "El Digimon '$DIGIMON_NAME' ya existe."
    exit 1
fi

# ============================================================================
# GENERACIÓN DE NOMBRES (Python-based para compatibilidad total)
# ============================================================================

# Genera CamelCase real (ej: my-digimon -> MyDigimon)
DIGIMON_CAMEL=$(python3 -c "import sys; print(''.join(x.capitalize() for x in sys.argv[1].replace('-', ' ').split()))" "$DIGIMON_NAME")

# Genera Role Display (ej: data-protector -> Data Protector)
ROLE_DISPLAY=$(python3 -c "import sys; print(sys.argv[1].replace('-', ' ').title())" "$ROLE")

print_header "Generando Digimon: $DIGIMON_NAME ($DIGIMON_CAMEL)"
mkdir -p "$DIGIMON_PATH"/{src/$DIGIMON_NAME,tests,docs,examples,.github/workflows}
print_success "Directorios creados"

# ============================================================================
# FUNCIÓN DE REEMPLAZO (macOS BSD sed compatible)
# ============================================================================

replace_in_file() {
    local file="$1"
    local old="$2"
    local new="$3"
    # Escapar para sed
    new=$(echo "$new" | sed 's/[&/\]/\\&/g')
    # BSD sed
    sed -i '' "s|$old|$new|g" "$file"
}

# ============================================================================
# 1. README.md
# ============================================================================
cat > "$DIGIMON_PATH/README.md" << EOF
# 🎮 $DIGIMON_CAMEL - $ROLE_DISPLAY

**Misión RDR2**: $MISSION  
**Rol de Ciberseguridad**: $ROLE  
**Estado**: Rookie (v$VERSION)  
**Mantenedor**: $AUTHOR  

## 🎯 Propósito
$DESCRIPTION

## 🚀 Inicio Rápido
\`\`\`bash
pip install -e .
\`\`\`

\`\`\`python
from $DIGIMON_NAME import $DIGIMON_CAMEL
digimon = $DIGIMON_CAMEL()
digimon.analyze()
\`\`\`
EOF
print_success "README.md generado"

# ============================================================================
# 2. pyproject.toml
# ============================================================================
LICENSE_CLASSIFIER=$([ "$LICENSE" = "MIT" ] && echo "MIT" || echo "Apache Software License")

cat > "$DIGIMON_PATH/pyproject.toml" << EOF
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[project]
name = "$DIGIMON_NAME"
version = "$VERSION"
description = "$DESCRIPTION"
readme = "README.md"
license = {text = "$LICENSE"}
authors = [{name = "$AUTHOR", email = "andresbarbudo@icloud.com"}]
requires-python = ">=3.10"

[project.urls]
Repository = "https://github.com/Andrei-Barwood/digimon-sec"

[tool.poetry]
packages = [{include = "$DIGIMON_NAME", from = "src"}]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
EOF
print_success "pyproject.toml generado"

# ============================================================================
# 3. src/__init__.py
# ============================================================================
cat > "$DIGIMON_PATH/src/$DIGIMON_NAME/__init__.py" << EOF
"""
$DIGIMON_CAMEL - Cybersecurity Module
"""
__version__ = "$VERSION"
from .core import $DIGIMON_CAMEL
__all__ = ["$DIGIMON_CAMEL", "__version__"]
EOF
print_success "src/__init__.py generado"

# ============================================================================
# 4. src/core.py
# ============================================================================
cat > "$DIGIMON_PATH/src/$DIGIMON_NAME/core.py" << EOF
"""
Core functionality for $DIGIMON_CAMEL
"""
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

class $DIGIMON_CAMEL:
    """
    $DIGIMON_CAMEL - $ROLE_DISPLAY
    Misión: $MISSION
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.name = "$DIGIMON_CAMEL"
        self.mission = "$MISSION"
        self.role = "$ROLE"
        self.config = config or {}
        logger.info(f"Initialized {self.name}")
    
    def analyze(self, data: Any = None) -> Dict[str, Any]:
        """Main analysis function"""
        return {
            "status": "success",
            "message": f"{self.name} analysis completed",
            "data": {}
        }
    
    def validate(self, data: Any) -> bool:
        """Validate input"""
        return True
    
    def get_info(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "role": self.role,
            "status": "Rookie"
        }

# Alias
Digimon = $DIGIMON_CAMEL
EOF
print_success "src/core.py generado"

# ============================================================================
# 5. tests/test_core.py
# ============================================================================
mkdir -p "$DIGIMON_PATH/tests"
touch "$DIGIMON_PATH/tests/__init__.py"

cat > "$DIGIMON_PATH/tests/test_core.py" << EOF
"""
Unit tests for $DIGIMON_CAMEL
"""
import pytest
from $DIGIMON_NAME.core import $DIGIMON_CAMEL

@pytest.fixture
def digimon():
    return $DIGIMON_CAMEL()

def test_initialization(digimon):
    assert digimon.name == "$DIGIMON_CAMEL"
    assert digimon.role == "$ROLE"

def test_analyze(digimon):
    result = digimon.analyze()
    assert result["status"] == "success"
EOF
print_success "tests/test_core.py generado"

# ============================================================================
# 6. Archivos extra (simplificados)
# ============================================================================
touch "$DIGIMON_PATH/requirements.txt"
touch "$DIGIMON_PATH/LICENSE"
touch "$DIGIMON_PATH/.gitignore"
mkdir -p "$DIGIMON_PATH/examples"
cat > "$DIGIMON_PATH/examples/basic_usage.py" << EOF
from $DIGIMON_NAME.core import $DIGIMON_CAMEL
print($DIGIMON_CAMEL().get_info())
EOF

print_header "✅ DIGIMON GENERADO: $DIGIMON_CAMEL"
echo "Ubicación: $DIGIMON_PATH"
echo "¡Listo para desarrollar!"
