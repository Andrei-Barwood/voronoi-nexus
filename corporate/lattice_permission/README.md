# Lattice Permission

Módulo **permissions** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lattice_permission
```

O desde el monorepo:

```bash
cd corporate/lattice_permission
pip install -e .
```

## Uso

```python
from lattice_permission.core import LatticePermission

result = LatticePermission().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
