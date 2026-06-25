# Torus Redact

Módulo **redaction** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install torus_redact
```

O desde el monorepo:

```bash
cd corporate/torus_redact
pip install -e .
```

## Uso

```python
from torus_redact.core import TorusRedact

result = TorusRedact().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
