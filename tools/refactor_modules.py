#!/usr/bin/env python3
"""
Refactor all corporate to Snocomm module names per corporate/manifest.yaml.
Run from repo root: python tools/refactor_modules.py
Creates new dirs under corporate/<folder_name>, then removes legacy corporate/<legacy_folder>.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Optional, Tuple


def parse_manifest(manifest_path: Path) -> list[dict]:
    """Parse manifest.yaml (simple parser, no PyYAML)."""
    text = manifest_path.read_text()
    modules = []
    current = None
    for line in text.splitlines():
        line = line.rstrip()
        if line.startswith("  - legacy_folder:"):
            if current:
                modules.append(current)
            current = {"legacy_folder": line.split(":", 1)[1].strip()}
        elif current is not None and line.startswith("    "):
            key, _, value = line.strip().partition(":")
            if key and value.strip():
                current[key] = value.strip()
    if current:
        modules.append(current)
    return modules


def get_old_package_dir(src_dir: Path) -> Optional[str]:
    """Return the single package directory name under src/ (e.g. compliancemon or Mnemomon)."""
    if not src_dir.exists():
        return None
    dirs = [d.name for d in src_dir.iterdir() if d.is_dir() and (d / "core.py").exists()]
    return dirs[0] if len(dirs) == 1 else (dirs[0] if dirs else None)


def get_old_class_and_display(core_path: Path) -> Tuple[Optional[str], Optional[str]]:
    """Extract class name and self.name value from core.py."""
    content = core_path.read_text()
    class_m = re.search(r"^class\s+(\w+)\s*[:(]", content, re.MULTILINE)
    name_m = re.search(r'self\.name\s*=\s*["\']([^"\']+)["\']', content)
    return (
        class_m.group(1) if class_m else None,
        name_m.group(1) if name_m else None,
    )


def get_old_import_name(pyproject_path: Path) -> Optional[str]:
    """Get package include name from [tool.poetry] packages."""
    if not pyproject_path.exists():
        return None
    text = pyproject_path.read_text()
    m = re.search(r'include\s*=\s*["\']([^"\']+)["\']', text)
    return m.group(1) if m else None


def transform_content(
    content: str,
    *,
    old_class: str,
    new_class: str,
    old_display: str,
    new_display: str,
    old_import: str,
    new_import: str,
    old_package_dir: str,
    new_package_name: str,
    old_folder: str,
    new_folder: str,
) -> str:
    """Apply all replacements for Snocomm rebrand."""
    # Order matters: do longer / more specific first
    content = content.replace(old_class, new_class)
    content = content.replace(old_display, new_display)
    content = content.replace(old_import, new_import)
    content = content.replace(old_package_dir, new_package_name)
    content = content.replace(old_folder, new_folder)

    content = re.sub(r"\bmóduloConfig\b", "ModuleConfig", content)
    content = re.sub(r"\bmóduloInfo\b", "ModuleInfo", content)
    content = re.sub(r'"módulo name"', '"Module name"', content)
    content = re.sub(r"description=\"módulo name\"", "description=\"Module name\"", content)
    # In ModuleConfig, set name default to display name
    content = re.sub(
        r'name:\s*str\s*=\s*Field\s*\(\s*default=["\'][^"\']*["\']',
        f'name: str = Field(default="{new_display}"',
        content,
        count=1,
    )
    content = re.sub(r"Snocomm Security Suite", "Snocomm Security Suite", content, flags=re.IGNORECASE)
    content = re.sub(r"modulo-sec-suite", "voronoi-nexus", content, flags=re.IGNORECASE)
    content = re.sub(r"snocomm-security-suite", "voronoi-nexus", content, flags=re.IGNORECASE)
    content = re.sub(r"modulo.sec.suite", "snocomm.security.suite", content, flags=re.IGNORECASE)

    # Remove or replace "módulo = OldClass" alias line
    content = re.sub(
        r"\n# Alias para retrocompatibilidad\s*\nmódulo = " + re.escape(old_class) + r"\s*\n",
        "\n",
        content,
    )
    content = re.sub(r"\n\s*módulo = " + re.escape(old_class) + r"\s*\n", "\n", content)

    # In docstrings/comments replace "módulo" with "módulo" where it refers to the entity
    content = re.sub(r"(\b)módulo(\b)", r"\1módulo\2", content)
    content = re.sub(r"información del módulo", "información del módulo", content, flags=re.IGNORECASE)
    content = re.sub(r"metadata del módulo", "metadata del módulo", content, flags=re.IGNORECASE)
    content = re.sub(r"información del módulo", "información del módulo", content)

    # In code: variable "modulo" -> "mod" in examples/tests (optional, keep for readability in fixtures)
    # We'll leave variable names as-is in fixtures (modulo -> mod would break fixture names). Only in examples.
    return content


def refactor_module(project_root: Path, entry: dict) -> bool:
    """Refactor one module: create new dir with transformed files, then remove old dir."""
    legacy = entry["legacy_folder"]
    new_folder = entry["folder_name"]
    new_package = entry["package_name"]
    new_class = entry["class_name"]
    new_display = entry["display_name"]

    old_path = project_root / "corporate" / legacy
    new_path = project_root / "corporate" / new_folder

    if not old_path.exists():
        print(f"  Skip (missing): {legacy}")
        return False
    if new_path.exists():
        print(f"  Skip (already exists): {new_folder}")
        return False

    src_old = old_path / "src"
    old_package_dir = get_old_package_dir(src_old)
    if not old_package_dir:
        print(f"  Skip (no src package): {legacy}")
        return False

    core_py = src_old / old_package_dir / "core.py"
    if not core_py.exists():
        print(f"  Skip (no core.py): {legacy}")
        return False

    old_class, old_display = get_old_class_and_display(core_py)
    if not old_class:
        print(f"  Skip (no class in core): {legacy}")
        return False
    if not old_display:
        old_display = old_class  # fallback

    old_import = get_old_import_name(old_path / "pyproject.toml") or legacy.replace("-", "_")
    if old_import == "Mnemomon":
        old_import = "mnemomon"  # pyproject says mnemomon

    # Build new tree
    new_src = new_path / "src" / new_package
    new_src.mkdir(parents=True, exist_ok=True)

    def transform(s: str) -> str:
        return transform_content(
            s,
            old_class=old_class,
            new_class=new_class,
            old_display=old_display,
            new_display=new_display,
            old_import=old_import,
            new_import=new_package,
            old_package_dir=old_package_dir,
            new_package_name=new_package,
            old_folder=legacy,
            new_folder=new_folder,
        )

    # Copy and transform Python files under src/old_package
    old_pkg_path = src_old / old_package_dir
    for f in old_pkg_path.iterdir():
        if f.suffix == ".py":
            new_src.joinpath(f.name).write_text(transform(f.read_text()), encoding="utf-8")

    # pyproject.toml
    pyproject = old_path / "pyproject.toml"
    if pyproject.exists():
        toml = pyproject.read_text()
        toml = re.sub(r'name\s*=\s*["\'][^"\']+["\']', f'name = "{new_package}"', toml, count=1)
        toml = re.sub(r'include\s*=\s*["\'][^"\']+["\']', f'include = "{new_package}"', toml)
        toml = re.sub(r"from\s*=\s*[\"']src[\"']", 'from = "src"', toml)
        toml = re.sub(r"modulo-sec-suite", "voronoi-nexus", toml, flags=re.IGNORECASE)
        toml = re.sub(r"snocomm-security-suite", "voronoi-nexus", toml, flags=re.IGNORECASE)
        toml = re.sub(
            r"(modulo-sec-suite|snocomm-security-suite)\.readthedocs\.io",
            "github.com/Andrei-Barwood/voronoi-nexus#readme",
            toml,
            flags=re.IGNORECASE,
        )
        toml = re.sub(
            r"https://github\.com/snocomm-security/(modulo-sec-suite|snocomm-security-suite)",
            "https://github.com/Andrei-Barwood/voronoi-nexus",
            toml,
            flags=re.IGNORECASE,
        )
        toml = transform(toml)
        # Fix Repository path
        toml = re.sub(r"tree/main/corporate/[^\s\]\"]+", f"tree/main/corporate/{new_folder}", toml)
        new_path.joinpath("pyproject.toml").write_text(toml, encoding="utf-8")

    # docs
    docs_old = old_path / "docs"
    if docs_old.exists():
        new_docs = new_path / "docs"
        new_docs.mkdir(parents=True, exist_ok=True)
        for f in docs_old.iterdir():
            if f.is_file():
                new_docs.joinpath(f.name).write_text(transform(f.read_text()), encoding="utf-8")

    # examples
    examples_old = old_path / "examples"
    if examples_old.exists():
        new_examples = new_path / "examples"
        new_examples.mkdir(parents=True, exist_ok=True)
        for f in examples_old.iterdir():
            if f.is_file():
                new_examples.joinpath(f.name).write_text(transform(f.read_text()), encoding="utf-8")

    # tests
    tests_old = old_path / "tests"
    if tests_old.exists():
        new_tests = new_path / "tests"
        new_tests.mkdir(parents=True, exist_ok=True)
        for f in tests_old.iterdir():
            if f.is_file():
                new_tests.joinpath(f.name).write_text(transform(f.read_text()), encoding="utf-8")

    # README.md at module root
    readme = old_path / "README.md"
    if readme.exists():
        new_path.joinpath("README.md").write_text(transform(readme.read_text()), encoding="utf-8")

    # Copy other top-level files (CHANGELOG, LICENSE, .gitignore, etc.)
    for f in old_path.iterdir():
        if f.is_file() and f.name not in ("pyproject.toml", "README.md"):
            new_path.joinpath(f.name).write_text(
                transform(f.read_text()) if f.suffix in (".md", ".txt", ".toml", ".yml", ".yaml") else f.read_text(),
                encoding="utf-8",
            )

    # Copy .github if present
    gh = old_path / ".github"
    if gh.exists():
        shutil.copytree(gh, new_path / ".github", dirs_exist_ok=True)
        for wf in (new_path / ".github" / "workflows").iterdir():
            if wf.is_file():
                wf.write_text(transform(wf.read_text()), encoding="utf-8")

    # Remove old directory
    shutil.rmtree(old_path)
    print(f"  OK: {legacy} -> {new_folder}")
    return True


def main():
    project_root = Path(__file__).resolve().parents[1]
    manifest_path = project_root / "corporate" / "manifest.yaml"
    if not manifest_path.exists():
        print("manifest.yaml not found")
        return
    modules = parse_manifest(manifest_path)
    print(f"Refactoring {len(modules)} modules...")
    for entry in modules:
        refactor_module(project_root, entry)
    print("Done.")


if __name__ == "__main__":
    main()
