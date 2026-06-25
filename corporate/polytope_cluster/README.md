# Polytope Cluster

Módulo **kubernetes** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install polytope_cluster
```

O desde el monorepo:

```bash
cd corporate/polytope_cluster
pip install -e .
```

## Uso

```python
from polytope_cluster.core import PolytopeCluster

result = PolytopeCluster().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
