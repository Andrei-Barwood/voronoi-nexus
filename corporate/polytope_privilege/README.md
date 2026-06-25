# Polytope Privilege

Módulo **privileges** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install polytope_privilege
```

O desde el monorepo:

```bash
cd corporate/polytope_privilege
pip install -e .
```

## Uso

```python
from polytope_privilege.core import PolytopePrivilege

result = PolytopePrivilege().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
