# Fractal Veil

Módulo **privacy** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install fractal_veil
```

O desde el monorepo:

```bash
cd corporate/fractal_veil
pip install -e .
```

## Uso

```python
from fractal_veil.core import FractalVeil

result = FractalVeil().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
