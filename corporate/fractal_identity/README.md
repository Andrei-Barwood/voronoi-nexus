# Fractal Identity

Módulo **identity** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install fractal_identity
```

O desde el monorepo:

```bash
cd corporate/fractal_identity
pip install -e .
```

## Uso

```python
from fractal_identity.core import FractalIdentity

result = FractalIdentity().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
