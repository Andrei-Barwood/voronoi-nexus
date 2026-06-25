# Tesseract Health

Módulo **hipaa** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install tesseract_health
```

O desde el monorepo:

```bash
cd corporate/tesseract_health
pip install -e .
```

## Uso

```python
from tesseract_health.core import TesseractHealth

result = TesseractHealth().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
