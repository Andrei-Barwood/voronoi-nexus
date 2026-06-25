# Geodesic Session

Módulo **sessions** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install geodesic_session
```

O desde el monorepo:

```bash
cd corporate/geodesic_session
pip install -e .
```

## Uso

```python
from geodesic_session.core import GeodesicSession

result = GeodesicSession().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
