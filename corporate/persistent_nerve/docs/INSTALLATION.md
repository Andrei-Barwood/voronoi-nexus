# Guía de Instalación - persistent_nerve

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install persistent_nerve
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/persistent_nerve
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from persistent_nerve.core import PersistentNerve

mod = PersistentNerve()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
