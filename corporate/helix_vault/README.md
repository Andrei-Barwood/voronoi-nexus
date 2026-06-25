# Helix Vault

Módulo **rds** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install helix_vault
```

O desde el monorepo:

```bash
cd corporate/helix_vault
pip install -e .
```

## Uso

```python
from helix_vault.core import HelixVault

result = HelixVault().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
