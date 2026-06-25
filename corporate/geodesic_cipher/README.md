# Geodesic Cipher

Módulo **encryption** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install geodesic_cipher
```

O desde el monorepo:

```bash
cd corporate/geodesic_cipher
pip install -e .
```

## Uso

```python
from geodesic_cipher.core import GeodesicCipher

result = GeodesicCipher().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
