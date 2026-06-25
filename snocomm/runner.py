"""Execute module operations (info, analyze) with signature-aware kwargs."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
from typing import Any

from snocomm.loader import load_class
from snocomm.manifest import ModuleMeta


def _is_optional(annotation: Any) -> bool:
    text = str(annotation)
    return "Optional" in text or annotation is type(None)


def build_analyze_kwargs(func: Any, overrides: dict[str, Any]) -> dict[str, Any]:
    """Build kwargs for analyze(), filling required params with safe demo defaults."""
    sig = inspect.signature(func)
    kwargs: dict[str, Any] = {}

    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if name in overrides and overrides[name] is not None:
            kwargs[name] = overrides[name]
            continue
        if param.default is not inspect.Parameter.empty:
            continue
        if _is_optional(param.annotation):
            continue
        annotation = str(param.annotation)
        if "Dict" in annotation:
            kwargs[name] = {}
        elif "List" in annotation:
            kwargs[name] = []
        elif "str" in annotation:
            kwargs[name] = "demo"
        elif "bytes" in annotation:
            kwargs[name] = b"demo"
        else:
            kwargs[name] = None

    return kwargs


def merge_overrides(
    input_path: Path | None,
    text: str | None,
    ioc: str | None,
    iocs: str | None,
    action: str | None,
    extra_json: str | None,
) -> dict[str, Any]:
    overrides: dict[str, Any] = {}

    if input_path:
        overrides.update(json.loads(input_path.read_text(encoding="utf-8")))

    if extra_json:
        overrides.update(json.loads(extra_json))

    if text is not None:
        overrides["text"] = text
        overrides.setdefault("content", text)

    if ioc is not None:
        overrides["ioc"] = ioc

    if iocs:
        parsed = [item.strip() for item in iocs.split(",") if item.strip()]
        overrides["iocs"] = parsed
        overrides.setdefault("urls", parsed)

    if action is not None:
        overrides["action"] = action

    return overrides


def serialize_result(result: Any) -> dict[str, Any]:
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if isinstance(result, dict):
        return result
    return {"result": repr(result)}


def run_info(meta: ModuleMeta, config: dict[str, Any] | None = None) -> dict[str, Any]:
    cls = load_class(meta)
    instance = cls(config)
    info = instance.get_info()
    if isinstance(info, dict):
        return info
    return {"info": str(info)}


def run_analyze(
    meta: ModuleMeta,
    config: dict[str, Any] | None = None,
    overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cls = load_class(meta)
    instance = cls(config)
    analyze = instance.analyze
    kwargs = build_analyze_kwargs(analyze, overrides or {})
    result = analyze(**kwargs)
    payload = serialize_result(result)
    return {
        "module": meta.folder_name,
        "display_name": meta.display_name,
        "domain": meta.domain,
        "input": kwargs,
        "result": payload,
    }
