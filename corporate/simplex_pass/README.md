# Simplex Pass

Módulo **passwords** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install simplex_pass
```

O desde el monorepo:

```bash
cd corporate/simplex_pass
pip install -e .
```

## Uso

```python
from simplex_pass.core import SimplexPass

result = SimplexPass().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
