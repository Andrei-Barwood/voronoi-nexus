# Guía de Instalación - helix_standard

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install helix_standard
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/helix_standard
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from helix_standard.core import HelixStandard

modulo = HelixStandard()
print(modulo.get_info())
```

---

Ver también: [PRESENTACION_CORPORATIVA.md](PRESENTACION_CORPORATIVA.md) (documento para comprador), [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
