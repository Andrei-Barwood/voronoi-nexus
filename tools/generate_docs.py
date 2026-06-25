#!/usr/bin/env python3
"""
Script para generar documentación automáticamente para todos los módulos Snocomm (Versión Mejorada)

Uso:
    python tools/generate_docs.py
    python tools/generate_docs.py --modulo <nombre>
    python tools/generate_docs.py --overwrite
"""

import argparse
import ast
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Union

# Plantillas de documentos mejoradas
INSTALLATION_TEMPLATE = """# Guía de Instalación - {name}

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install {name}
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/{name}
python -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from {import_name}.core import {class_name}

mod = {class_name}()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
"""

USAGE_TEMPLATE = """# Guía de Uso - {name}

## Inicio Rápido

### Instalación

```bash
pip install -e .
```

### Uso Básico

```python
from {import_name}.core import {class_name}

# Crear instancia
mod = {class_name}()

# Ejecutar análisis principal
# Nota: Revise API.md para ver los argumentos específicos de analyze()
result = mod.analyze()
print(result)
```

## Configuración Avanzada

Puede configurar {name} pasando un diccionario al constructor:

```python
mod = {class_name}(config={{
{config_example}
}})
```

## Ejemplos de Uso

### Análisis Completo

```python
from {import_name}.core import {class_name}

mod = {class_name}()

# Ejecutar análisis (ajuste los parámetros según sus necesidades)
result = mod.analyze()

if result.status == "success":
    print(f"Operación exitosa: {{result.message}}")
    print("Datos:", result.data)
elif result.status == "warning":
    print(f"Advertencia: {{result.message}}")
else:
    print(f"Error: {{result.message}}")
    print("Errores:", result.errors)
```

### Validación de Datos

```python
data = "..." # Datos a validar
if mod.validate(data):
    print("Datos válidos para procesamiento")
else:
    print("Datos inválidos")
```

## Mejores Prácticas (2025-2026)

1. **Configuración Mínima**: Comience con la configuración por defecto y ajuste según necesidad.
2. **Manejo de Errores**: Verifique siempre `result.status` antes de procesar `result.data`.
3. **Logs**: Configure el nivel de logging adecuado para producción vs desarrollo.
4. **Validación**: Use el método `validate()` antes de procesar datos externos no confiables.

---

Ver también: [ARCHITECTURE.md](ARCHITECTURE.md), [API.md](API.md)
"""

API_TEMPLATE = """# API Reference - {name}

## Class: {class_name}

### Constructor

```python
{class_name}(config: Optional[Dict[str, Any]] = None)
```

**Parámetros de Configuración:**

{config_params_doc}

### Métodos Principales

{methods_doc}

## Modelos de Datos

{models_doc}

---

Ver también: [USAGE.md](USAGE.md), [ARCHITECTURE.md](ARCHITECTURE.md)
"""

ARCHITECTURE_TEMPLATE = """# Arquitectura - {name}

## Visión General

{name} es un módulo de ciberseguridad implementado como parte del **Snocomm Security Suite**.

- **Misión**: {mission}
- **Rol de Seguridad**: {role}
- **Nivel**: Production (v3.0.0)
- **Versión**: 3.0.0

## Propósito

{description}

## Estructura del Componente

### 1. Core Module (`core.py`)

La clase `{class_name}` es el punto de entrada principal. Implementa la lógica de negocio y orquesta las operaciones de seguridad.

**Responsabilidades:**
{methods_list}

### 2. Models (`models.py`)

Define la estructura de datos utilizando **Pydantic v2**, asegurando validación estricta y serialización segura.

**Modelos Principales:**
{models_list}

### 3. Utils (`utils.py`)

Proporciona utilidades auxiliares como configuración de logging y helpers comunes.

## Configuración y Personalización

El módulo se configura mediante un diccionario inmutable (`frozen=True` en Pydantic) pasado al inicializador.

```python
config = {{
{config_example}
}}
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
"""

def extract_config_from_init(content: str) -> List[Dict[str, str]]:
    """Intenta extraer parámetros de configuración del __init__ analizando el código."""
    config_params = []
    
    # Buscar patrones como: self.algo = config.get("algo", valor)
    # o self.algo = self.config.get("algo", valor)
    matches = re.findall(r'self\.(\w+)\s*=\s*(?:self\.)?config\.get\(\s*["\'](\w+)["\']\s*,\s*([^)]+)\)', content)
    
    for attr, key, default in matches:
        # Limpiar el valor por defecto
        default = default.strip()
        desc = f"Configura {attr}" # Descripción genérica si no hay docstring
        config_params.append({
            "name": key,
            "default": default,
            "description": desc
        })
        
    return config_params

def extract_modulo_info(modulo_path: Path) -> Dict[str, Any]:
    """Extrae información detallada del modulo mediante análisis AST y Regex."""
    info = {
        "name": modulo_path.name,
        "class_name": "",
        "mission": "No especificada",
        "role": "No especificado",
        "description": "",
        "methods": [],
        "config_params": [],
        "models": [],
        "import_name": modulo_path.name
    }

    # 1. Analizar __init__.py
    # Buscar el directorio del paquete real dentro de src
    src_dir = modulo_path / "src"
    package_dir = None
    
    if src_dir.exists():
        # Intentar con el nombre del modulo
        potential_package = src_dir / modulo_path.name
        if potential_package.exists():
            package_dir = potential_package
        else:
            # Intentar normalizando nombre (guiones a guiones bajos)
            normalized_name = modulo_path.name.replace("-", "_")
            potential_package = src_dir / normalized_name
            if potential_package.exists():
                package_dir = potential_package
            else:
                # Si no, tomar el primer directorio que encuentre
                subdirs = [d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
                if subdirs:
                    package_dir = subdirs[0]

    if not package_dir:
        print(f"⚠️  No se encontró el paquete fuente en {src_dir}")
        return info
        
    info["import_name"] = package_dir.name
    init_file = package_dir / "__init__.py"
    if init_file.exists():
        content = init_file.read_text(encoding='utf-8')
        
        # Misión y Rol
        m_mission = re.search(r'Misión:\s*(.+)', content)
        if m_mission: info["mission"] = m_mission.group(1).strip()
        
        m_role = re.search(r'Rol:\s*(.+)', content)
        if m_role: info["role"] = m_role.group(1).strip()
        
        # Class Name
        m_class = re.search(r'from\s+\.core\s+import\s+(\w+)', content)
        if m_class: info["class_name"] = m_class.group(1)

    # 2. Analizar core.py
    core_file = package_dir / "core.py"
    if core_file.exists():
        content = core_file.read_text(encoding='utf-8')
        
        # Descripción
        m_desc = re.search(r'Descripción:\s*(.+?)(?:\n\s+""")', content, re.DOTALL)
        if m_desc:
            desc = m_desc.group(1).strip()
            # Limpiar indentación excesiva
            desc = re.sub(r'\n\s+', '\n', desc)
            info["description"] = desc
        elif not info["description"]:
             # Intentar obtener del docstring del módulo
             m_mod_desc = re.search(r'^"""\s*(.+?)\s*"""', content, re.DOTALL)
             if m_mod_desc:
                 info["description"] = m_mod_desc.group(1).split('\n')[0]

        # Análisis AST para métodos
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == info["class_name"]:
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                            # Obtener firma del método
                            args = [arg.arg for arg in item.args.args if arg.arg != 'self']
                            
                            # Obtener tipos si existen
                            arg_types = []
                            for arg in item.args.args:
                                if arg.arg != 'self' and arg.annotation:
                                    # Simplificación muy básica de tipos
                                    arg_types.append(f"{arg.arg}") 
                            
                            docstring = ast.get_docstring(item)
                            info["methods"].append({
                                "name": item.name,
                                "args": ", ".join(args),
                                "docstring": docstring or "Sin documentación.",
                                "signature": f"def {item.name}({', '.join(args)})"
                            })
        except Exception as e:
            print(f"Error analizando AST de core.py: {e}")

        # Extraer configuración del __init__ usando Regex (más robusto que AST para esto a veces)
        m_init = re.search(r'def __init__.*?config.*?:\s*(.+?)(?:\n\s+""")', content, re.DOTALL)
        if m_init:
            config_doc = m_init.group(1)
            params = re.findall(r'- (\w+):\s*(.+?)(?:\n|$)', config_doc)
            for p_name, p_desc in params:
                info["config_params"].append({"name": p_name, "description": p_desc.strip(), "default": "N/A"})
        
        # Si no encontró en docstring, intentar inferir del código
        if not info["config_params"]:
            info["config_params"] = extract_config_from_init(content)

    # 3. Analizar models.py
    models_file = package_dir / "models.py"
    if models_file.exists():
        content = models_file.read_text(encoding='utf-8')
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Ignorar ConfigDict o clases internas de Pydantic si aparecen
                    if node.name in ["ConfigDict", "BaseModel"]: continue
                    
                    docstring = ast.get_docstring(node)
                    fields = []
                    
                    # Intentar extraer campos (muy básico)
                    for item in node.body:
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            fields.append(item.target.id)
                            
                    info["models"].append({
                        "name": node.name,
                        "docstring": docstring or "",
                        "fields": fields
                    })
        except Exception as e:
            print(f"Error analizando AST de models.py: {e}")

    return info

def generate_docs(modulo_path: Path, overwrite: bool = False) -> bool:
    """Genera los documentos para un modulo."""
    docs_dir = modulo_path / "docs"
    docs_dir.mkdir(exist_ok=True)

    info = extract_modulo_info(modulo_path)
    
    if not info["class_name"]:
        print(f"⚠️  No se pudo determinar la clase principal para {modulo_path.name}. Saltando.")
        return False

    name = info["name"]
    class_name = info["class_name"]
    import_name = info["import_name"] # Usualmente igual al nombre de carpeta, pero en imports Python usa _ a veces. Asumimos nombre carpeta es paquete.

    # Preparar strings para templates
    
    # Configuración
    config_example_lines = []
    config_params_doc_lines = []
    
    if info["config_params"]:
        for param in info["config_params"]:
            default_val = param.get("default", "N/A")
            # Tratar de formatear el default si parece string
            config_example_lines.append(f'    "{param["name"]}": {default_val},  # {param.get("description", "")}')
            config_params_doc_lines.append(f"- `{param['name']}`: {param.get('description', '')} (Default: `{default_val}`)")
    else:
        config_example_lines.append('    # "opcion": "valor",  # Configuración específica')
        config_params_doc_lines.append("- No hay parámetros de configuración específicos documentados.")

    config_example = "\n".join(config_example_lines)
    config_params_doc = "\n".join(config_params_doc_lines)

    # Métodos
    methods_doc = ""
    methods_list_arch = ""
    for method in info["methods"]:
        methods_doc += f"#### `{method['name']}({method['args']})`\n\n"
        methods_doc += f"{method['docstring']}\n\n"
        
        # Resumen para arquitectura
        summary = method['docstring'].split('.')[0] if method['docstring'] else "Operación del módulo"
        methods_list_arch += f"- `{method['name']}()`: {summary}\n"

    # Modelos
    models_doc = ""
    models_list_arch = ""
    for model in info["models"]:
        models_doc += f"### {model['name']}\n\n"
        if model["docstring"]:
            models_doc += f"{model['docstring']}\n\n"
        if model["fields"]:
            models_doc += "**Campos:**\n"
            for field in model["fields"]:
                models_doc += f"- `{field}`\n"
        models_doc += "\n"
        
        summary = model['docstring'].split('.')[0] if model['docstring'] else "Modelo de datos"
        models_list_arch += f"- `{model['name']}`: {summary}\n"

    # Generar Archivos
    
    # INSTALLATION.md
    if not (docs_dir / "INSTALLATION.md").exists() or overwrite:
        (docs_dir / "INSTALLATION.md").write_text(INSTALLATION_TEMPLATE.format(
            name=name, import_name=import_name, class_name=class_name
        ), encoding='utf-8')
        print(f"✅ Generado: INSTALLATION.md para {name}")

    # USAGE.md
    if not (docs_dir / "USAGE.md").exists() or overwrite:
        (docs_dir / "USAGE.md").write_text(USAGE_TEMPLATE.format(
            name=name, import_name=import_name, class_name=class_name, config_example=config_example
        ), encoding='utf-8')
        print(f"✅ Generado: USAGE.md para {name}")

    # API.md
    if not (docs_dir / "API.md").exists() or overwrite:
        (docs_dir / "API.md").write_text(API_TEMPLATE.format(
            name=name, class_name=class_name, config_params_doc=config_params_doc,
            methods_doc=methods_doc, models_doc=models_doc
        ), encoding='utf-8')
        print(f"✅ Generado: API.md para {name}")

    # ARCHITECTURE.md
    if not (docs_dir / "ARCHITECTURE.md").exists() or overwrite:
        (docs_dir / "ARCHITECTURE.md").write_text(ARCHITECTURE_TEMPLATE.format(
            name=name, mission=info["mission"], role=info["role"],
            description=info["description"] or f"{name} proporciona capacidades avanzadas de seguridad.",
            class_name=class_name, methods_list=methods_list_arch,
            models_list=models_list_arch, config_example=config_example
        ), encoding='utf-8')
        print(f"✅ Generado: ARCHITECTURE.md para {name}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Generador de Documentación Snocomm")
    parser.add_argument("--modulo", "-d", type=str, help="Nombre del módulo (carpeta en corporate/)")
    parser.add_argument("--overwrite", "-o", action="store_true", help="Sobrescribir archivos existentes")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    corporate_dir = project_root / "corporate"

    if args.modulo:
        target_dir = corporate_dir / args.modulo
        if not target_dir.exists():
            print(f"❌ Módulo no encontrado: {args.modulo}")
            return
        generate_docs(target_dir, overwrite=args.overwrite)
    else:
        count = 0
        for d in sorted(corporate_dir.iterdir()):
            if d.is_dir() and (d / "src").exists():
                print(f"📦 Procesando {d.name}...")
                if generate_docs(d, overwrite=args.overwrite):
                    count += 1
        print(f"\n✨ Completado. Documentación generada para {count} módulos.")

if __name__ == "__main__":
    main()
