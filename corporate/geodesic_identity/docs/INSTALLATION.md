# Guia de Instalacion - geodesic_identity

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalacion desde PyPI

```bash
pip install geodesic_identity
```

## Instalacion desde Codigo Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/geodesic_identity
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificacion de Instalacion

```python
from geodesic_identity.core import GeodesicIdentity

modulo = GeodesicIdentity()
print(modulo.get_info())
```

---

Ver tambien: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)

