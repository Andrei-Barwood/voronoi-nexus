# Guía de Instalación - vertex_hook

## Requisitos Previos

- Python 3.10+
- pip o poetry
- Git

## Instalación desde PyPI

```bash
pip install vertex_hook
```

## Instalación desde Código Fuente

```bash
git clone https://github.com/Andrei-Barwood/voronoi-nexus.git
cd voronoi-nexus/corporate/vertex_hook
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

## Verificación de Instalación

```python
from vertex_hook.core import VertexHook

mod = VertexHook()
print(mod.get_info())
```

---

Ver también: [USAGE.md](USAGE.md), [API.md](API.md), [ARCHITECTURE.md](ARCHITECTURE.md)
