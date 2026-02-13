# Guía de Instalación - delaunay_sentinel

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install delaunay_sentinel
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/snocomm-security/snocomm-security-suite.git
cd snocomm-security-suite/corporate/delaunay_sentinel
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from delaunay_sentinel.core import DelaunaySentinel

mod = DelaunaySentinel()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
