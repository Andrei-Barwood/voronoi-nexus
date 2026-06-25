# Hyperplane Crawl

Módulo **scraping** del [Snocomm Security Suite](https://github.com/Andrei-Barwood/voronoi-nexus).

## Instalación

```bash
pip install hyperplane_crawl
```

O desde el monorepo:

```bash
cd corporate/hyperplane_crawl
pip install -e .
```

## Uso

```python
from hyperplane_crawl.core import HyperplaneCrawl

result = HyperplaneCrawl().analyze()
print(result.status, result.message)
```

## Documentación

Ver `docs/` para guías de instalación, API y arquitectura.
