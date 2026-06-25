# Lemniscate OAuth

Módulo **oauth** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lemniscate_oauth
```

O desde el monorepo:

```bash
cd corporate/lemniscate_oauth
pip install -e .
```

## Uso

```python
from lemniscate_oauth.core import LemniscateOauth

result = LemniscateOauth().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
