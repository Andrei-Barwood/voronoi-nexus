# Lemniscate Right

Módulo **gdpr** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lemniscate_right
```

O desde el monorepo:

```bash
cd corporate/lemniscate_right
pip install -e .
```

## Uso

```python
from lemniscate_right.core import LemniscateRight

result = LemniscateRight().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
