# Guía de Instalación - hausdorff_match

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install hausdorff_match
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/snocomm-security/snocomm-security-suite.git
cd snocomm-security-suite/corporate/hausdorff_match
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from hausdorff_match.core import HausdorffMatch

mod = HausdorffMatch()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
