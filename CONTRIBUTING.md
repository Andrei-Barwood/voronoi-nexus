# Guía para contribuir

Gracias por tu interés en contribuir al **Snocomm Security Suite**. Este documento describe cómo configurar el entorno y ejecutar los tests, y cómo añadir o modificar módulos (empresas filiales).

---

## Cómo clonar y ejecutar tests

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
   cd voronoi-nexus
   ```

2. Usa **Python 3.10 o superior** (el proyecto no es compatible con 3.9). Con [pyenv](https://github.com/pyenv/pyenv):
   ```bash
   pyenv install 3.10.3   # si aún no lo tienes
   pyenv local 3.10.3     # respeta .python-version en la raíz
   ```

3. Crea un entorno virtual (recomendado) e instala dependencias:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   pip install -e ".[dev]"
   ```
   Alternativa mínima solo para tests:
   ```bash
   pip install pytest pytest-cov pydantic
   ```

4. Ejecuta todos los tests de los módulos corporativos:
   ```bash
   ./tools/test_all_modules.sh
   ```
   o, con el runner en Python:
   ```bash
   python tools/test_all_modules.py
   python tools/test_all_modules.py --quiet    # solo resumen
   python tools/test_all_modules.py --verbose  # salida detallada
   ```

5. Ejecuta los tests de integración del pipeline y la CLI:
   ```bash
   pytest tests/ -v
   ```

6. Usa la CLI unificada `snocomm`:
   ```bash
   snocomm list
   snocomm info helix-filter
   snocomm run helix-filter --iocs evil-snake-oil.com,google.com
   snocomm pipeline --urls google.com --content "user@example.com"
   snocomm posture --output infra-posture-report.json
   python -m snocomm list --json
   ```

7. Construir ejecutable standalone (PyInstaller):
   ```bash
   pip install -e ".[executable]"
   python tools/build_executable.py --onefile --clean
   # Genera dist/snocomm-{linux|darwin|windows}-{arch}[.exe]
   # Guía para revisión de infra: docs/INFRA_POSTURE.md
   ```

---

## Naming Guide y registro de empresas

- El **Naming Guide** (convención de nombres: geometría + minimalismo/futurismo) está en el [README principal](README.md#naming-guide).
- La fuente de verdad de empresas, dominios y nombres técnicos es [corporate/manifest.yaml](corporate/manifest.yaml). Cualquier nueva empresa o cambio de identidad debe reflejarse ahí con: `folder_name`, `package_name`, `class_name`, `display_name`, `domain`.

---

## Estructura esperada de un módulo

Cada empresa/módulo bajo `corporate/` debe seguir esta estructura:

```
corporate/<folder_name>/
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── INSTALLATION.md
│   ├── PRESENTACION_CORPORATIVA.md
│   └── USAGE.md
├── examples/
│   ├── basic_usage.py
│   └── README.md
├── src/<package_name>/
│   ├── __init__.py
│   ├── core.py
│   ├── models.py
│   └── (opcional) utils.py
├── tests/
│   ├── conftest.py
│   └── test_core.py
├── pyproject.toml
├── LICENSE
└── README.md
```

- `folder_name` y `package_name` suelen coincidir (snake_case).
- La clase principal en `core.py` debe usar PascalCase (ej. `TesseractCovenant`).
- Los scripts en `tools/` (p. ej. `generate_docs.py`, `generate_presentaciones_corporativas.py`) usan el manifest para generar documentación; al añadir un módulo, regístralo en el manifest y regenera si aplica.

---

## Añadir un nuevo módulo

1. Elige un nombre según el [Naming Guide](README.md#naming-guide) y un dominio (ej. `compliance`, `iam`, `threat-intel`).
2. Añade una entrada en [corporate/manifest.yaml](corporate/manifest.yaml) con `folder_name`, `package_name`, `class_name`, `display_name`, `domain`. Si el módulo reemplaza uno legacy, puedes usar `legacy_folder` como referencia histórica.
3. Crea la carpeta `corporate/<folder_name>/` y copia la estructura de un módulo existente (p. ej. `tesseract_covenant` o `helix_filter`).
4. Implementa `core.py`, `models.py`, docs y tests. Asegura que `get_info()` devuelva `"status": "Production"` y que los tests pasen.
5. Opcional: ejecuta `python tools/generate_docs.py` y `python tools/generate_presentaciones_corporativas.py` si usas plantillas compartidas para documentación y presentaciones.

---

*Snocomm Security Suite — Contribuciones bienvenidas.*
