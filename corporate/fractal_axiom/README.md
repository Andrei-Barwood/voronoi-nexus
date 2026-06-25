# Fractal Axiom

Módulo **cloud-security** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install fractal_axiom
```

O desde el monorepo:

```bash
cd corporate/fractal_axiom
pip install -e .
```

## Uso

```python
from fractal_axiom.core import FractalAxiom

result = FractalAxiom().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
