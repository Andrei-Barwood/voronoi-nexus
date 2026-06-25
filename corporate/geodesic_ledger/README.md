# Geodesic Ledger

Módulo **cost** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install geodesic_ledger
```

O desde el monorepo:

```bash
cd corporate/geodesic_ledger
pip install -e .
```

## Uso

```python
from geodesic_ledger.core import GeodesicLedger

result = GeodesicLedger().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
