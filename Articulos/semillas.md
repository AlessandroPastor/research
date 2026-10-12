# Artículos semilla para el estado del arte (versión 2, 2026-10-09)

Fuente: búsquedas S1–S4 de Scopus (`FORMULAS_BUSQUEDA_SCOPUS.txt`). Son 565 registros; tras quitar duplicados
quedan 434, y el cribado deja **145 estudios primarios** (`criterios_inclusion_exclusion.md`, `cribado.csv`).
Todo se regenera con `python Articulos/analisis_scopus.py`.

Se usan dos criterios:
1. **Co-citación:** los trabajos que más citan los 145 estudios incluidos.
2. **Eje de la tesis:** un artículo reciente y revisado por pares por cada pilar del experimento.

## A. Trabajos base (más co-citados por los 145 incluidos)

| Trabajo | Estudios que lo citan | Clave en `referencias_nfr.bib` |
|---|---|---|
| Kurtanović y Maalej, RE 2017 | 71 | Kurtanovic2017-SupervisedML |
| NoRBERT (Hey et al.), RE 2020 | 65 | Hey2020-NoRBERT |
| BERT (Devlin et al.), NAACL 2019 | 55 | Devlin2019-BERT |
| Cleland-Huang et al., Req. Eng. 2007 | 48 | ClelandHuang2007-NFR |
| Alhoshan et al., IST 2023 (zero-shot) | 25 | Alhoshan2023-ZeroShot |
| SMOTE / EDA / TextAttack | 6 / 5 / 1 | Chawla2002-SMOTE / Wei2019-EDA / Morris2020-TextAttack |

## B. Semillas por eje de la tesis (dentro del corpus)

| Eje | Artículo | Fuente |
|---|---|---|
| Aumentación + BERT | Ben Ammar y Almatrafi, *TAOS: A Novel TextAttack Oversampling Approach…* (2025), 10.48084/etasr.14313 | ETASR (revista) |
| LLM como clasificador | Binkhonain y Alfayez, *Are prompts all you need? Evaluating prompt-based LLMs for software requirements classification* (2025), 10.1007/s00766-025-00451-8 | Requirements Engineering (Springer, revista) |
| BERT / PLM para NFR | Alhaizaey y Al-Mashari, *Automated Classification and Identification of NFR in Agile-Based Requirements Using Pre-Trained Language Models* (2025), 10.1109/ACCESS.2025.3570359 | IEEE Access |

Alternativas por si el grafo de alguna semilla sale pobre:
- Aumentación: Aldhafer et al. 2026 (10.1109/ACCESS.2026.3673382) y Limaylla-Lunarejo et al. 2026 (10.1007/s10664-025-10736-9, balanceo en español).
- Generación sintética con LLM: Pham et al., SEKE 2025 (10.18293/SEKE2025-123).
- LLM zero/few-shot: Shafikuzzaman et al. 2025 (10.1109/ACCESS.2025.3607813).

Nota: estos datos salen de los metadatos de Scopus (título, resumen y referencias). Antes de citar cualquier
resultado numérico hay que leer el texto completo.

## Uso en el estado del arte

Las semillas y figuras ya están en `EstadoArte/EstadoArte_NFR.tex` (sección II): Fig. 2 (flujo de
preselección), Fig. 3 (años), Fig. 4 (co-citación), Tabla I (semillas), Fig. 5 (mapa) y Fig. 6
(cobertura de ejes). Las claves del `.bib` son BenAmmar2025-TAOS, Binkhonain2025-Prompts,
Alhaizaey2025-AgilePLM y Alhoshan2023-ZeroShot.
