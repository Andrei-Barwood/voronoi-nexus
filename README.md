# Snocomm Security Suite

Snocomm es un holding de empresas especializadas en ciberseguridad. Cada empresa cubre un ámbito concreto: al contratar una de ellas, su organización obtiene un **área de trabajo dedicada** a ese dominio (cumplimiento, IAM, threat intelligence, forense, etc.), con producto, documentación y soporte alineados con los estándares actuales del sector.

Este repositorio contiene el **catálogo de empresas filiales**, el **Naming Guide** y la referencia de **dominios por empresa**.

---

## Naming Guide

El nombre de cada empresa Snocomm sigue una convención que combina:

1. **Un concepto de geometría avanzada**  
   Referencias a formas, estructuras o ideas matemáticas/geométricas (ej. tesseract, lemniscate, vértice, fractal, geodesia, toro, politopo, simplex, manifold, lattice, hélice, hiperplano).

2. **Una conclusión derivada de la filosofía futurista aplicada al minimalismo espiritual**  
   Ideas de horizonte, axioma, covenant, stillness, veil, trace, etc., que evocan claridad, propósito y visión a largo plazo sin ruido innecesario.

### Reglas prácticas

| Regla | Descripción |
|-------|-------------|
| **Longitud** | Máximo 3 palabras; idealmente 1 o 2. |
| **Formato** | Display: "Tesseract Covenant". Código: `tesseract_covenant` (snake_case), clase: `TesseractCovenant` (PascalCase). |
| **Ámbito** | El nombre no describe literalmente el producto (evita marcas genéricas); el **dominio** es lo que define el foco técnico. |
| **Coherencia** | Misma familia conceptual en todo el catálogo para reforzar la identidad Snocomm. |

### Ejemplos del catálogo

| Concepto geométrico | Idea minimalista/futurista | Empresa |
|--------------------|----------------------------|---------|
| Tesseract | Covenant, Health, Factor | Tesseract Covenant, Tesseract Health, Tesseract Factor |
| Lemniscate | Horizon, Archive, Right, Anon, OAuth, Mnemo | Lemniscate Horizon, Lemniscate Archive, Lemniscate Right, Lemniscate Anon, Lemniscate OAuth, Lemniscate Mnemo |
| Fractal | Axiom, Veil, Mask, SSO, Identity | Fractal Axiom, Fractal Veil, Fractal Mask, Fractal SSO, Fractal Identity |
| Vertex | Stillness, Hash, Auth, Credential, Vuln, Scan | Vertex Stillness, Vertex Hash, Vertex Auth, Vertex Credential, Vertex Vuln, Vertex Scan |
| Geodesic | Identity, Ledger, Cipher, Directory, Session, Network | Geodesic Identity, Geodesic Ledger, Geodesic Cipher, Geodesic Directory, Geodesic Session, Geodesic Network |
| Helix | Vault, Standard, Filter, Biometric, Incident, Trace | Helix Vault, Helix Standard, Helix Filter, Helix Biometric, Helix Incident, Helix Trace |
| Torus | Vault, Redact, Token, Log | Torus Vault, Torus Redact, Torus Token, Torus Log |
| Simplex | Container, Token, Secret, Pass, Cipher | Simplex Container, Simplex Token, Simplex Secret, Simplex Pass, Simplex Cipher |
| Polytope | Cluster, DLP, Privilege | Polytope Cluster, Polytope DLP, Polytope Privilege |
| Manifold | Code, Fuzz | Manifold Code, Manifold Fuzz |
| Lattice | Resource, Permission, Policy | Lattice Resource, Lattice Permission, Lattice Policy |
| Hyperplane | Guard, Crawl | Hyperplane Guard, Hyperplane Crawl |
| Voronoi | Reclaim | Voronoi Reclaim |
| Delaunay | Sentinel | Delaunay Sentinel |
| Simplicial | Swarm | Simplicial Swarm |
| Radon | Veilbreak | Radon Veilbreak |
| Elliptic | Proof | Elliptic Proof |
| Minkowski | Unpack | Minkowski Unpack |
| Kuratowski | Forge | Kuratowski Forge |
| Hausdorff | Match | Hausdorff Match |
| Affine | Replica | Affine Replica |
| Persistent | Nerve | Persistent Nerve |
| Helly | Rules | Helly Rules |

---

## Catálogo de empresas y dominios

Cada fila es una empresa filial de Snocomm. El **dominio** indica el ámbito técnico y de negocio; la **carpeta** es el nombre del módulo en este repositorio.

| Empresa (display name) | Dominio | Carpeta (módulo) |
|------------------------|---------|-------------------|
| Tesseract Covenant | compliance | `tesseract_covenant` |
| Lemniscate Horizon | compliance-cloud | `lemniscate_horizon` |
| Fractal Axiom | cloud-security | `fractal_axiom` |
| Geodesic Identity | iam | `geodesic_identity` |
| Vertex Stillness | vpc | `vertex_stillness` |
| Hyperplane Guard | firewall | `hyperplane_guard` |
| Torus Vault | s3 | `torus_vault` |
| Helix Vault | rds | `helix_vault` |
| Polytope Cluster | kubernetes | `polytope_cluster` |
| Simplex Container | docker | `simplex_container` |
| Manifold Code | iac | `manifold_code` |
| Lattice Resource | resource-usage | `lattice_resource` |
| Geodesic Ledger | cost | `geodesic_ledger` |
| Lemniscate Archive | backup | `lemniscate_archive` |
| Vertex Scan | scast | `vertex_scan` |
| Fractal Veil | privacy | `fractal_veil` |
| Helix Standard | pci-dss | `helix_standard` |
| Tesseract Health | hipaa | `tesseract_health` |
| Lemniscate Right | gdpr | `lemniscate_right` |
| Simplex Token | tokenization | `simplex_token` |
| Hyperplane Crawl | scraping | `hyperplane_crawl` |
| Fractal Mask | masking | `fractal_mask` |
| Vertex Hash | hashing | `vertex_hash` |
| Geodesic Cipher | encryption | `geodesic_cipher` |
| Lemniscate Anon | anonymization | `lemniscate_anon` |
| Torus Redact | redaction | `torus_redact` |
| Polytope DLP | dlp | `polytope_dlp` |
| Helix Filter | threat-intel | `helix_filter` |
| Simplex Secret | secrets | `simplex_secret` |
| Geodesic Directory | ldap | `geodesic_directory` |
| Vertex Auth | authentication | `vertex_auth` |
| Torus Token | tokens | `torus_token` |
| Lemniscate OAuth | oauth | `lemniscate_oauth` |
| Fractal SSO | sso | `fractal_sso` |
| Tesseract Factor | mfa | `tesseract_factor` |
| Polytope Privilege | privileges | `polytope_privilege` |
| Helix Biometric | biometrics | `helix_biometric` |
| Simplex Pass | passwords | `simplex_pass` |
| Geodesic Session | sessions | `geodesic_session` |
| Vertex Credential | credentials | `vertex_credential` |
| Lattice Permission | permissions | `lattice_permission` |
| Fractal Identity | identity | `fractal_identity` |
| Manifold Fuzz | fuzzing | `manifold_fuzz` |
| Helix Incident | incidents | `helix_incident` |
| Lattice Policy | policy | `lattice_policy` |
| Torus Log | logs | `torus_log` |
| Vertex Vuln | vulnerabilities | `vertex_vuln` |
| Geodesic Network | network | `geodesic_network` |
| Helix Trace | forensics | `helix_trace` |
| Simplex Cipher | cipher | `simplex_cipher` |
| Lemniscate Mnemo | mnemonic | `lemniscate_mnemo` |
| Voronoi Reclaim | ransomware-detection | `voronoi_reclaim` |
| Delaunay Sentinel | malware-analysis | `delaunay_sentinel` |
| Geodesic Pursuit | apt-hunting | `geodesic_pursuit` |
| Simplicial Swarm | botnet-tracking | `simplicial_swarm` |
| Radon Veilbreak | steganography-detection | `radon_veilbreak` |
| Elliptic Proof | crypto-analysis | `elliptic_proof` |
| Minkowski Unpack | packer-analysis | `minkowski_unpack` |
| Kuratowski Forge | disassembly | `kuratowski_forge` |
| Polytope Detonate | sandbox-detonation | `polytope_detonate` |
| Affine Replica | emulation | `affine_replica` |
| Persistent Nerve | behavior-analysis | `persistent_nerve` |
| Helly Rules | yara-engine | `helly_rules` |
| Hausdorff Match | signature-matching | `hausdorff_match` |

---

## Estructura del repositorio

```
corporate/
├── manifest.yaml              # Fuente de verdad: empresas, dominios, nombres técnicos
├── tesseract_covenant/        # Una carpeta por empresa
│   ├── docs/
│   │   ├── PRESENTACION_CORPORATIVA.md   # Documento para el comprador
│   │   ├── INSTALLATION.md
│   │   ├── USAGE.md
│   │   └── ...
│   ├── src/<package_name>/
│   └── ...
├── helix_filter/
├── ...
shared/                        # Pipeline que integra módulos (ej. Helix Filter + Simplex Secret)
tools/                         # Scripts de generación de docs y presentaciones
```

- **Documentación por empresa**: en cada `corporate/<carpeta>/docs/` encontrará la guía de instalación, uso, API, arquitectura y la **presentación corporativa** (documento para el comprador).
- **Catálogo y naming**: este README y `corporate/manifest.yaml` definen empresas, dominios y convención de nombres.

---

## Cómo usar este catálogo

1. **Por dominio**: busque en la tabla el **dominio** que necesita (ej. `threat-intel`, `compliance`, `iam`) y use la **carpeta** indicada para acceder al código y a la documentación.
2. **Por empresa**: si conoce el nombre de la empresa (ej. Helix Filter), localícela en la tabla para ver su dominio y carpeta.
3. **Naming para nuevas empresas**: al añadir una nueva filial, siga el [Naming Guide](#naming-guide) y registre `display_name`, `domain` y nombres técnicos en `corporate/manifest.yaml`.

---

*Snocomm Security Suite — Catálogo de empresas y dominios.*
