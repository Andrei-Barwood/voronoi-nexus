# Torus Vault

Módulo **s3** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install torus_vault
```

O desde el monorepo:

```bash
cd corporate/torus_vault
pip install -e .
```

## Uso

```python
from torus_vault.core import TorusVault

result = TorusVault().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
