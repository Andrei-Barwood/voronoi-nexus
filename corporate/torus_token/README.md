# Torus Token

Módulo **tokens** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install torus_token
```

O desde el monorepo:

```bash
cd corporate/torus_token
pip install -e .
```

## Uso

```python
from torus_token.core import TorusToken

result = TorusToken().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
