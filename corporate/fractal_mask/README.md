# Fractal Mask

Módulo **masking** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install fractal_mask
```

O desde el monorepo:

```bash
cd corporate/fractal_mask
pip install -e .
```

## Uso

```python
from fractal_mask.core import FractalMask

result = FractalMask().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
