"""Unified Snocomm command-line interface."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import click

from snocomm import __version__
from snocomm.manifest import load_manifest, resolve_module
from snocomm.posture import run_infra_posture
from snocomm.runner import merge_overrides, run_analyze, run_info


def _echo_json(data: Any) -> None:
    click.echo(json.dumps(data, indent=2, ensure_ascii=False, default=str))


def _load_config(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    return json.loads(path.read_text(encoding="utf-8"))


@click.group()
@click.version_option(version=__version__, prog_name="snocomm")
@click.pass_context
def main(ctx: click.Context) -> None:
    """Snocomm Security Suite — interfaz de línea de comandos unificada."""
    ctx.ensure_object(dict)
    ctx.obj["modules"] = load_manifest()


@main.command("list")
@click.option("--domain", help="Filtrar por dominio (ej. threat-intel, iam)")
@click.option("--json", "as_json", is_flag=True, help="Salida en JSON")
@click.pass_context
def list_modules(ctx: click.Context, domain: str | None, as_json: bool) -> None:
    """Lista los módulos disponibles del catálogo."""
    modules = ctx.obj["modules"]
    if domain:
        modules = [m for m in modules if m.domain == domain]

    if as_json:
        _echo_json(
            [
                {
                    "cli_name": m.cli_name,
                    "folder_name": m.folder_name,
                    "display_name": m.display_name,
                    "domain": m.domain,
                }
                for m in modules
            ]
        )
        return

    click.echo(f"Snocomm Security Suite — {len(modules)} módulos\n")
    for module in modules:
        click.echo(f"  {module.cli_name:<28} {module.display_name:<28} [{module.domain}]")


@main.command("info")
@click.argument("module")
@click.option(
    "--config", type=click.Path(exists=True, path_type=Path), help="JSON de configuración"
)
@click.option("--json", "as_json", is_flag=True, help="Salida en JSON")
@click.pass_context
def info(ctx: click.Context, module: str, config: Path | None, as_json: bool) -> None:
    """Muestra metadata de un módulo (get_info)."""
    meta = resolve_module(module, ctx.obj["modules"])
    if meta is None:
        raise click.ClickException(f"Módulo no encontrado: {module}")

    payload = {
        "module": meta.folder_name,
        "cli_name": meta.cli_name,
        "display_name": meta.display_name,
        "domain": meta.domain,
        "info": run_info(meta, _load_config(config)),
    }

    if as_json:
        _echo_json(payload)
        return

    click.echo(f"{payload['display_name']} ({payload['cli_name']})")
    click.echo(f"Dominio: {payload['domain']}\n")
    for key, value in payload["info"].items():
        click.echo(f"  {key}: {value}")


@main.command("run")
@click.argument("module")
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="JSON de configuración del módulo",
)
@click.option(
    "--input",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    help="JSON con argumentos para analyze()",
)
@click.option("--data", "extra_json", help="JSON inline con argumentos para analyze()")
@click.option("--text", help="Texto de entrada (text/content)")
@click.option("--ioc", help="IOC único")
@click.option("--iocs", help="Lista de IOCs separados por coma")
@click.option("--action", help="Acción para módulos con parámetro action")
@click.option("--json", "as_json", is_flag=True, help="Salida en JSON")
@click.pass_context
def run(
    ctx: click.Context,
    module: str,
    config: Path | None,
    input_path: Path | None,
    extra_json: str | None,
    text: str | None,
    ioc: str | None,
    iocs: str | None,
    action: str | None,
    as_json: bool,
) -> None:
    """Ejecuta analyze() en un módulo."""
    meta = resolve_module(module, ctx.obj["modules"])
    if meta is None:
        raise click.ClickException(f"Módulo no encontrado: {module}")

    overrides = merge_overrides(input_path, text, ioc, iocs, action, extra_json)

    try:
        payload = run_analyze(meta, _load_config(config), overrides)
    except Exception as exc:
        raise click.ClickException(f"Error ejecutando {meta.cli_name}: {exc}") from exc

    if as_json:
        _echo_json(payload)
        return

    result = payload["result"]
    status = result.get("status", "ok")
    message = result.get("message", "")
    click.echo(f"[{status.upper()}] {payload['display_name']}")
    if message:
        click.echo(message)
    if result.get("data"):
        click.echo("\nDatos:")
        for key, value in result["data"].items():
            click.echo(f"  {key}: {value}")


@main.command("pipeline")
@click.option("--urls", required=True, help="URLs/IPs separadas por coma")
@click.option("--content", default="", help="Contenido de tráfico a analizar")
@click.option("--json", "as_json", is_flag=True, help="Salida en JSON")
def pipeline(urls: str, content: str, as_json: bool) -> None:
    """Ejecuta el pipeline integrado (Helix Filter + Simplex Secret)."""
    from shared.pipeline import SecurityPipeline

    url_list = [item.strip() for item in urls.split(",") if item.strip()]
    result = SecurityPipeline().process_traffic(url_list, content)

    if as_json:
        _echo_json(result)
        return

    click.echo(f"Estado: {result['status']}")
    click.echo(f"Fase: {result['phase_completed']}")
    summary = result.get("summary", {})
    for key, value in summary.items():
        click.echo(f"  {key}: {value}")


@main.command("posture")
@click.option(
    "--config",
    type=click.Path(exists=True, path_type=Path),
    help="JSON de configuración compartida para los módulos",
)
@click.option(
    "--input",
    "input_path",
    type=click.Path(exists=True, path_type=Path),
    help="JSON con overrides por módulo: {\"vertex_vuln\": {...}}",
)
@click.option(
    "--output",
    "output_path",
    type=click.Path(path_type=Path),
    help="Guardar reporte JSON en archivo",
)
@click.option("--json", "as_json", is_flag=True, help="Salida en JSON")
def posture(
    config: Path | None,
    input_path: Path | None,
    output_path: Path | None,
    as_json: bool,
) -> None:
    """Evalúa postura de seguridad de infraestructura interna (17 controles)."""
    input_overrides = None
    if input_path:
        input_overrides = json.loads(input_path.read_text(encoding="utf-8"))

    report = run_infra_posture(config=_load_config(config), input_overrides=input_overrides)

    if output_path:
        output_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n",
            encoding="utf-8",
        )

    if as_json or output_path:
        if as_json:
            _echo_json(report)
        elif output_path:
            click.echo(f"Reporte guardado en {output_path}")
        return

    click.echo("Snocomm — Infrastructure Security Posture")
    if report.get("data_mode") == "demo_baseline":
        click.echo("(Modo demo — usa --input con datos reales de tu infraestructura)\n")
    click.echo(f"Nivel: {report['posture_level']}  |  Score: {report['overall_score']}/100")
    click.echo(
        f"Controles: {report['summary']['total_checks']}  "
        f"(OK: {report['summary']['passed']}, "
        f"Warnings: {report['summary']['warnings']}, "
        f"Failed: {report['summary']['failed']})\n"
    )

    for category, data in sorted(report["categories"].items()):
        click.echo(f"## {category.upper()} — score {data['score']}/100")
        for check in data["checks"]:
            click.echo(
                f"  [{check['status'].upper():7}] {check['display_name']:<28} {check['focus']}"
            )
        click.echo()

    if report["priority_actions"]:
        click.echo("Acciones prioritarias:")
        for item in report["priority_actions"]:
            click.echo(f"  - {item['module']} ({item['category']}): {item['reason']}")


@main.command("domains")
@click.option("--json", "as_json", is_flag=True, help="Salida en JSON")
@click.pass_context
def domains(ctx: click.Context, as_json: bool) -> None:
    """Lista dominios técnicos con conteo de módulos."""
    modules = ctx.obj["modules"]
    counts: dict[str, int] = {}
    for module in modules:
        counts[module.domain] = counts.get(module.domain, 0) + 1

    if as_json:
        _echo_json(counts)
        return

    click.echo("Dominios disponibles:\n")
    for domain, count in sorted(counts.items()):
        click.echo(f"  {domain:<40} {count} módulo(s)")


if __name__ == "__main__":
    main()
