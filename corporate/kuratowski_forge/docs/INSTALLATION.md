# Guía de Instalación - kuratowski_forge

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install kuratowski_forge
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/snocomm-security/snocomm-security-suite.git
cd snocomm-security-suite/corporate/kuratowski_forge
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from kuratowski_forge.core import KuratowskiForge

mod = KuratowskiForge()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
