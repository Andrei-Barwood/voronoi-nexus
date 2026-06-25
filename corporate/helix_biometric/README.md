# Helix Biometric

Módulo **biometrics** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install helix_biometric
```

O desde el monorepo:

```bash
cd corporate/helix_biometric
pip install -e .
```

## Uso

```python
from helix_biometric.core import HelixBiometric

result = HelixBiometric().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
