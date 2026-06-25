# Simplex Container

Módulo **docker** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install simplex_container
```

O desde el monorepo:

```bash
cd corporate/simplex_container
pip install -e .
```

## Uso

```python
from simplex_container.core import SimplexContainer

result = SimplexContainer().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
