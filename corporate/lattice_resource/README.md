# Lattice Resource

Módulo **resource-usage** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lattice_resource
```

O desde el monorepo:

```bash
cd corporate/lattice_resource
pip install -e .
```

## Uso

```python
from lattice_resource.core import LatticeResource

result = LatticeResource().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
