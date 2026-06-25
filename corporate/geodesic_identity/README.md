# Geodesic Identity

Módulo **iam** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install geodesic_identity
```

O desde el monorepo:

```bash
cd corporate/geodesic_identity
pip install -e .
```

## Uso

```python
from geodesic_identity.core import GeodesicIdentity

result = GeodesicIdentity().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
