# Lemniscate Horizon

Módulo **compliance-cloud** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lemniscate_horizon
```

O desde el monorepo:

```bash
cd corporate/lemniscate_horizon
pip install -e .
```

## Uso

```python
from lemniscate_horizon.core import LemniscateHorizon

result = LemniscateHorizon().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
