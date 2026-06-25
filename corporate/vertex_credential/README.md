# Vertex Credential

Módulo **credentials** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install vertex_credential
```

O desde el monorepo:

```bash
cd corporate/vertex_credential
pip install -e .
```

## Uso

```python
from vertex_credential.core import VertexCredential

result = VertexCredential().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
