# Lemniscate Anon

Módulo **anonymization** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install lemniscate_anon
```

O desde el monorepo:

```bash
cd corporate/lemniscate_anon
pip install -e .
```

## Uso

```python
from lemniscate_anon.core import LemniscateAnon

result = LemniscateAnon().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
