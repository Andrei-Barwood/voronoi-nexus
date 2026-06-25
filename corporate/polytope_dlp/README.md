# Polytope DLP

Módulo **dlp** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install polytope_dlp
```

O desde el monorepo:

```bash
cd corporate/polytope_dlp
pip install -e .
```

## Uso

```python
from polytope_dlp.core import PolytopeDlp

result = PolytopeDlp().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
