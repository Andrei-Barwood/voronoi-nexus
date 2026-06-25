#!/usr/bin/env python3
"""Genera README.md mínimos para módulos que no lo tienen (requerido por poetry build)."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

README_TEMPLATE = """# {display_name}

Módulo **{domain}** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install {package_name}
```

O desde el monorepo:

```bash
cd corporate/{folder_name}
pip install -e .
```

## Uso

```python
from {package_name}.core import {class_name}

result = {class_name}().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
"""


def parse_manifest(manifest_path: Path) -> list[dict[str, str]]:
    modules: list[dict[str, str]] = []
    current: dict[str, str] = {}
    key_map = {
        "folder_name": "folder_name",
        "package_name": "package_name",
        "class_name": "class_name",
        "display_name": "display_name",
        "domain": "domain",
    }

    for raw_line in manifest_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- legacy_folder:"):
            if current.get("folder_name"):
                modules.append(current)
            current = {}
            continue
        for yaml_key, field in key_map.items():
            if line.startswith(f"{yaml_key}:"):
                current[field] = line.split(":", 1)[1].strip()
                break

    if current.get("folder_name"):
        modules.append(current)
    return modules


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera README.md faltantes en corporate/")
    parser.add_argument("--dry-run", action="store_true", help="Solo listar módulos sin README")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    corporate = root / "corporate"
    manifest = corporate / "manifest.yaml"
    if not manifest.exists():
        print("No se encontró corporate/manifest.yaml", file=sys.stderr)
        return 1

    by_folder = {m["folder_name"]: m for m in parse_manifest(manifest)}
    created = 0

    for folder, meta in sorted(by_folder.items()):
        module_dir = corporate / folder
        readme = module_dir / "README.md"
        if readme.exists():
            continue
        if not module_dir.is_dir():
            print(f"  Skip (sin carpeta): {folder}")
            continue
        if args.dry_run:
            print(f"  Faltaría README: {folder}")
            created += 1
            continue
        readme.write_text(
            README_TEMPLATE.format(
                display_name=meta.get("display_name", folder),
                domain=meta.get("domain", "security"),
                package_name=meta.get("package_name", folder),
                class_name=meta.get("class_name", folder.title().replace("_", "")),
                folder_name=folder,
            ),
            encoding="utf-8",
        )
        print(f"  ✅ README creado: {folder}")
        created += 1

    print(f"\nTotal: {created} README(s) {'pendientes' if args.dry_run else 'creados'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())