"""Dynamic import of corporate security modules."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Any, Type

from snocomm.manifest import ModuleMeta, project_root


def module_src_path(meta: ModuleMeta) -> Path:
    return project_root() / "corporate" / meta.folder_name / "src"


def ensure_module_path(meta: ModuleMeta) -> Path:
    src = module_src_path(meta)
    if not src.is_dir():
        raise FileNotFoundError(f"Module source not found: {src}")
    src_str = str(src)
    if src_str not in sys.path:
        sys.path.insert(0, src_str)
    return src


def load_class(meta: ModuleMeta) -> Type[Any]:
    ensure_module_path(meta)
    module = importlib.import_module(f"{meta.package_name}.core")
    cls = getattr(module, meta.class_name, None)
    if cls is None:
        raise AttributeError(f"{meta.class_name} not found in {meta.package_name}.core")
    return cls
