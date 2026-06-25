# Lemniscate Archive

Módulo **backup** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lemniscate_archive
```

O desde el monorepo:

```bash
cd corporate/lemniscate_archive
pip install -e .
```

## Uso

```python
from lemniscate_archive.core import LemniscateArchive

result = LemniscateArchive().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
