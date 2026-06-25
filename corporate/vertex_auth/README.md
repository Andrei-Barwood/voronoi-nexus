# Vertex Auth

Módulo **authentication** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install vertex_auth
```

O desde el monorepo:

```bash
cd corporate/vertex_auth
pip install -e .
```

## Uso

```python
from vertex_auth.core import VertexAuth

result = VertexAuth().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
