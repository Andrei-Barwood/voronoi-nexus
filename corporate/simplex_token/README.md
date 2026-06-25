# Simplex Token

Módulo **tokenization** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install simplex_token
```

O desde el monorepo:

```bash
cd corporate/simplex_token
pip install -e .
```

## Uso

```python
from simplex_token.core import SimplexToken

result = SimplexToken().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
