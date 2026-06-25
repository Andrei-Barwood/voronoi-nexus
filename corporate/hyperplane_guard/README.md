# Hyperplane Guard

Módulo **firewall** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install hyperplane_guard
```

O desde el monorepo:

```bash
cd corporate/hyperplane_guard
pip install -e .
```

## Uso

```python
from hyperplane_guard.core import HyperplaneGuard

result = HyperplaneGuard().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
