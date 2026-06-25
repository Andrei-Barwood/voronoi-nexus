"""Load module metadata from corporate/manifest.yaml."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from snocomm.paths import project_root


@dataclass(frozen=True)
class ModuleMeta:
    folder_name: str
    package_name: str
    class_name: str
    display_name: str
    domain: str

    @property
    def cli_name(self) -> str:
        return self.folder_name.replace("_", "-")


def load_manifest(manifest_path: Path | None = None) -> list[ModuleMeta]:
    path = manifest_path or (project_root() / "corporate" / "manifest.yaml")
    if not path.exists():
        raise FileNotFoundError(f"Manifest not found: {path}")

    modules: list[ModuleMeta] = []
    current: dict[str, str] = {}
    key_map = {
        "folder_name": "folder_name",
        "package_name": "package_name",
        "class_name": "class_name",
        "display_name": "display_name",
        "domain": "domain",
    }

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if line.startswith("- legacy_folder:"):
            if current.get("folder_name"):
                modules.append(ModuleMeta(**current))  # type: ignore[arg-type]
            current = {}
            continue
        for yaml_key, field in key_map.items():
            if line.startswith(f"{yaml_key}:"):
                current[field] = line.split(":", 1)[1].strip()
                break

    if current.get("folder_name"):
        modules.append(ModuleMeta(**current))  # type: ignore[arg-type]

    return modules


def resolve_module(name: str, modules: list[ModuleMeta]) -> ModuleMeta | None:
    normalized = name.strip().lower().replace("-", "_")
    for module in modules:
        if module.folder_name == normalized or module.cli_name == name.strip().lower():
            return module
    return None
