# Guía de Instalación - geodesic_pursuit

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install geodesic_pursuit
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/snocomm-security/snocomm-security-suite.git
cd snocomm-security-suite/corporate/geodesic_pursuit
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from geodesic_pursuit.core import GeodesicPursuit

mod = GeodesicPursuit()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
