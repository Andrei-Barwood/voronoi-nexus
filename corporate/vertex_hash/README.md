# Vertex Hash

Módulo **hashing** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install vertex_hash
```

O desde el monorepo:

```bash
cd corporate/vertex_hash
pip install -e .
```

## Uso

```python
from vertex_hash.core import VertexHash

result = VertexHash().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
