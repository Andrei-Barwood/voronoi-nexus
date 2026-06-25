# Vertex Stillness

Módulo **vpc** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install vertex_stillness
```

O desde el monorepo:

```bash
cd corporate/vertex_stillness
pip install -e .
```

## Uso

```python
from vertex_stillness.core import VertexStillness

result = VertexStillness().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
