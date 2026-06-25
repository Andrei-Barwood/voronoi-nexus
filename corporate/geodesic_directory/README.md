# Geodesic Directory

Módulo **ldap** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install geodesic_directory
```

O desde el monorepo:

```bash
cd corporate/geodesic_directory
pip install -e .
```

## Uso

```python
from geodesic_directory.core import GeodesicDirectory

result = GeodesicDirectory().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
