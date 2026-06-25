# Tesseract Covenant

Módulo **compliance** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install tesseract_covenant
```

O desde el monorepo:

```bash
cd corporate/tesseract_covenant
pip install -e .
```

## Uso

```python
from tesseract_covenant.core import TesseractCovenant

result = TesseractCovenant().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
