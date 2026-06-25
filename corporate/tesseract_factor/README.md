# Tesseract Factor

Módulo **mfa** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install tesseract_factor
```

O desde el monorepo:

```bash
cd corporate/tesseract_factor
pip install -e .
```

## Uso

```python
from tesseract_factor.core import TesseractFactor

result = TesseractFactor().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
