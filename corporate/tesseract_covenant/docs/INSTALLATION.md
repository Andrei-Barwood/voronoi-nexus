# Guía de Instalación - tesseract_covenant

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install tesseract_covenant
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/tesseract_covenant
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from tesseract_covenant.core import TesseractCovenant

modulo = TesseractCovenant()
print(modulo.get_info())
```

---

Ver también: [PRESENTACION_CORPORATIVA.md](PRESENTACION_CORPORATIVA.md) (documento para comprador), [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
