# Guia de Instalacion - torus_vault

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalacion desde PyPI

```bash
pip install torus_vault
```

## Instalacion desde Codigo Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/torus_vault
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificacion de Instalacion

```python
from torus_vault.core import TorusVault

modulo = TorusVault()
print(modulo.get_info())
```

---

Ver tambien: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)

