#!/usr/bin/env python3
"""
Empaqueta módulos Snocomm por lotes para GitHub Releases.

Genera por cada módulo:
  - wheel (.whl) — distribución binaria Python (pip install)
  - sdist (.tar.gz) — código fuente empaquetado

Genera por lote:
  - ZIP consolidado con todos los artefactos del lote
  - SHA256SUMS
  - build-report.json

Uso:
    python tools/ensure_module_readmes.py
    python tools/package_release_batch.py --list
    python tools/package_release_batch.py --batch 1
    python tools/package_release_batch.py --all
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class ModuleBuildResult:
    folder: str
    success: bool
    version: str | None = None
    wheel: str | None = None
    sdist: str | None = None
    error: str | None = None


@dataclass
class BatchBuildResult:
    batch_id: int
    batch_name: str
    title: str
    version: str
    modules: list[ModuleBuildResult] = field(default_factory=list)

    @property
    def passed(self) -> int:
        return sum(1 for m in self.modules if m.success)

    @property
    def failed(self) -> int:
        return sum(1 for m in self.modules if not m.success)


def load_release_config(config_path: Path) -> dict[str, Any]:
    text = config_path.read_text(encoding="utf-8")
    version_match = re.search(r'^version:\s*["\']?([^"\'\n]+)', text, re.MULTILINE)
    suite_version = version_match.group(1).strip() if version_match else "1.0.0"

    batches: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    in_modules = False

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("- id:"):
            if current:
                batches.append(current)
            current = {"id": int(line.split(":", 1)[1].strip())}
            in_modules = False
            continue
        if current is None:
            continue
        if line.startswith("name:") and not in_modules:
            current["name"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("title:"):
            current["title"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("modules:"):
            in_modules = True
            current.setdefault("modules", [])
        elif in_modules and line.startswith("- "):
            current.setdefault("modules", []).append(line[2:].strip())

    if current:
        batches.append(current)

    return {"version": suite_version, "batches": batches}


def read_module_version(pyproject: Path) -> str | None:
    if not pyproject.exists():
        return None
    match = re.search(r'^version\s*=\s*["\']([^"\']+)["\']', pyproject.read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else None


def build_module(module_dir: Path, python_exe: str) -> ModuleBuildResult:
    folder = module_dir.name
    pyproject = module_dir / "pyproject.toml"
    version = read_module_version(pyproject)

    if not pyproject.exists():
        return ModuleBuildResult(folder=folder, success=False, version=version, error="Sin pyproject.toml")

    dist_dir = module_dir / "dist"
    if dist_dir.exists():
        shutil.rmtree(dist_dir)

    try:
        proc = subprocess.run(
            [python_exe, "-m", "build", "--outdir", str(dist_dir)],
            cwd=module_dir,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return ModuleBuildResult(folder=folder, success=False, version=version, error="Timeout (>5 min)")

    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "build failed").strip()
        return ModuleBuildResult(folder=folder, success=False, version=version, error=err[-800:])

    wheels = sorted(dist_dir.glob("*.whl"))
    sdists = sorted(dist_dir.glob("*.tar.gz"))
    if not wheels and not sdists:
        return ModuleBuildResult(folder=folder, success=False, version=version, error="dist/ vacío")

    return ModuleBuildResult(
        folder=folder,
        success=True,
        version=version,
        wheel=wheels[-1].name if wheels else None,
        sdist=sdists[-1].name if sdists else None,
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_artifacts(module_dir: Path, staging: Path) -> list[Path]:
    collected: list[Path] = []
    dist_dir = module_dir / "dist"
    if not dist_dir.exists():
        return collected
    for artifact in sorted(dist_dir.iterdir()):
        if artifact.suffix in {".whl"} or artifact.name.endswith(".tar.gz"):
            dest = staging / artifact.name
            shutil.copy2(artifact, dest)
            collected.append(dest)
    return collected


def create_batch_zip(staging: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(staging.iterdir()):
            if file.is_file():
                zf.write(file, arcname=file.name)


def write_checksums(directory: Path) -> Path:
    sums_path = directory / "SHA256SUMS"
    lines: list[str] = []
    for file in sorted(directory.iterdir()):
        if file.name == "SHA256SUMS":
            continue
        if file.is_file():
            lines.append(f"{sha256_file(file)}  {file.name}")
    sums_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return sums_path


def package_batch(
    batch: dict[str, Any],
    suite_version: str,
    corporate_dir: Path,
    output_root: Path,
    python_exe: str,
) -> BatchBuildResult:
    batch_id = int(batch["id"])
    batch_name = batch["name"]
    title = batch.get("title", batch_name)
    result = BatchBuildResult(
        batch_id=batch_id,
        batch_name=batch_name,
        title=title,
        version=suite_version,
    )

    batch_dir = output_root / f"batch{batch_id}-{batch_name}-v{suite_version}"
    staging = batch_dir / "artifacts"
    staging.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 60}")
    print(f"📦 Lote {batch_id}: {title}")
    print(f"{'=' * 60}")

    for folder in batch["modules"]:
        module_dir = corporate_dir / folder
        print(f"  Building {folder}...", end=" ", flush=True)
        mod_result = build_module(module_dir, python_exe)
        result.modules.append(mod_result)
        if mod_result.success:
            collect_artifacts(module_dir, staging)
            print(f"✅ {mod_result.wheel or mod_result.sdist}")
        else:
            print(f"❌ {mod_result.error}")

    zip_name = f"snocomm-batch{batch_id}-{batch_name}-v{suite_version}.zip"
    zip_path = batch_dir / zip_name
    create_batch_zip(staging, zip_path)
    write_checksums(batch_dir)

    report = {
        "batch_id": batch_id,
        "batch_name": batch_name,
        "title": title,
        "suite_version": suite_version,
        "built_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "total": len(result.modules),
            "passed": result.passed,
            "failed": result.failed,
        },
        "modules": [
            {
                "folder": m.folder,
                "success": m.success,
                "version": m.version,
                "wheel": m.wheel,
                "sdist": m.sdist,
                "error": m.error,
            }
            for m in result.modules
        ],
        "artifacts_zip": zip_name,
    }
    (batch_dir / "build-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"\n  Artefactos: {batch_dir}")
    print(f"  ZIP: {zip_path.name} ({zip_path.stat().st_size / 1024:.1f} KiB)")
    print(f"  Módulos OK: {result.passed}/{len(result.modules)}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Empaqueta módulos Snocomm por lotes")
    parser.add_argument("--batch", type=int, help="ID de lote (1-6)")
    parser.add_argument("--all", action="store_true", help="Empaquetar todos los lotes")
    parser.add_argument("--list", action="store_true", help="Listar lotes disponibles")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Directorio de salida (default: dist/releases)",
    )
    parser.add_argument("--python", default=sys.executable, help="Intérprete Python para build")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    config_path = root / "corporate" / "release_batches.yaml"
    corporate_dir = root / "corporate"
    output_root = args.output or (root / "dist" / "releases")

    if not config_path.exists():
        print(f"No se encontró {config_path}", file=sys.stderr)
        return 1

    config = load_release_config(config_path)
    batches = {int(b["id"]): b for b in config["batches"]}
    suite_version = config["version"]

    if args.list:
        print(f"Snocomm Release Batches v{suite_version}\n")
        for bid in sorted(batches):
            b = batches[bid]
            print(f"  [{bid}] {b.get('title', b['name'])} — {len(b['modules'])} módulos")
        return 0

    if not args.all and args.batch is None:
        parser.print_help()
        return 1

    # Verificar que `build` está disponible
    check = subprocess.run([args.python, "-m", "build", "--version"], capture_output=True, text=True)
    if check.returncode != 0:
        print("Instala el paquete build: pip install build", file=sys.stderr)
        return 1

    selected = sorted(batches) if args.all else [args.batch]
    for bid in selected:
        if bid not in batches:
            print(f"Lote inválido: {bid}. Usa --list para ver opciones.", file=sys.stderr)
            return 1

    output_root.mkdir(parents=True, exist_ok=True)
    results: list[BatchBuildResult] = []

    for bid in selected:
        results.append(package_batch(batches[bid], suite_version, corporate_dir, output_root, args.python))

    total_failed = sum(r.failed for r in results)
    print(f"\n{'=' * 60}")
    print(f"RESUMEN: {len(results)} lote(s), {total_failed} módulo(s) fallidos")
    print(f"Salida: {output_root}")
    print(f"{'=' * 60}")

    return 1 if total_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())