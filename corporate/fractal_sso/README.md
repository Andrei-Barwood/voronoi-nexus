# Fractal SSO

Módulo **sso** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install fractal_sso
```

O desde el monorepo:

```bash
cd corporate/fractal_sso
pip install -e .
```

## Uso

```python
from fractal_sso.core import FractalSso

result = FractalSso().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
