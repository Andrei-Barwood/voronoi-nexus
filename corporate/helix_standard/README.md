# Helix Standard

Módulo **pci-dss** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install helix_standard
```

O desde el monorepo:

```bash
cd corporate/helix_standard
pip install -e .
```

## Uso

```python
from helix_standard.core import HelixStandard

result = HelixStandard().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
