# Manifold Code

Módulo **iac** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install manifold_code
```

O desde el monorepo:

```bash
cd corporate/manifold_code
pip install -e .
```

## Uso

```python
from manifold_code.core import ManifoldCode

result = ManifoldCode().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
