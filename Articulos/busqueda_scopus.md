# Estrategia de búsqueda en Scopus (versión 2, 2026-10-08)

Sustituye a los scripts 1–7 anteriores. Cada búsqueda está pensada para copiarse tal cual en
*Scopus → Advanced document search*.

## 1. Problemas de los scripts anteriores

| # | Problema | Efecto observado en las exportaciones del 2026-10-02 |
|---|---|---|
| 1 | Siglas ambiguas sueltas: `"NFR"`, `"SRS"`, `"EDA"` | SRS y EDA tienen otros significados en otras áreas (en medicina, por ejemplo). 30 registros traen "SRS" sin referirse a *software requirements specification*, y 26 ni siquiera contienen la palabra *requirement*: revisiones clínicas, satélites, plagas de pinos… |
| 2 | Falta el concepto **clasificación** | Con `"software requirement*" AND "LLM" AND "deep learning"` entra cualquier artículo de IA generativa en ingeniería de requerimientos. |
| 3 | Mezcla de roles del LLM: `"LLM"` aparece en el bloque de aumentación | En la tesis el LLM es **clasificador**, no generador, pero la búsqueda trae trabajos de generación de requisitos. |
| 4 | Años y filtros distintos en cada script (>2017, >2018, >2019, >2021; COMP sí/no) | Los conteos PRISMA no son comparables ni reproducibles. |
| 5 | `LIMIT-TO (SUBJAREA,"COMP")` | Deja fuera trabajos clasificados solo en *Engineering*. |
| 6 | No se excluyen las *Conference review* | 28 registros eran volúmenes completos de actas (REFSQ, ICBDA…), no artículos. |
| 7 | `"PROMISE"` suelto (script 6) | Coincide con la palabra inglesa *promise* ("shows promise"). |
| 8 | `"nonfunctional"` (sin guion) no está | Se pierden los artículos que lo escriben así. |
| 9 | No hay búsqueda para el paso 5 de la tesis (GitHub / auto-etiquetado) | Ese pilar queda sin respaldo bibliográfico. |
| 10 | El script 7 (XAI: LIME/SHAP) | No forma parte del flujo experimental de la tesis. Se elimina, salvo que el asesor pida explicabilidad. |

## 2. Diseño

Todas las búsquedas comparten un **bloque núcleo (R)**: *clasificación de requerimientos no funcionales o de
software*. Cada búsqueda le suma **un eje** de la tesis:

| Búsqueda | Eje | Paso de la tesis |
|---|---|---|
| S1 | Aumentación y desbalance (TAOS, EDA, SMOTE-Tomek) | 1 |
| S2 | BERT y transformers | 2 |
| S3 | LLM como clasificador | 3 |
| S4 | Ampliación con GitHub y auto-etiquetado | 5 |
| S5 | **Núcleo directo** = S1 ∩ (S2 ∪ S3): los competidores directos | 1–3 |

Los filtros son los mismos en todas: 2017–2026, artículos, ponencias, revisiones y capítulos, en inglés o español.

**Prueba del bloque R:** se aplicó a los 253 registros ya exportados. Pasan 122 y **se conservan los 50
estudios preseleccionados**. Las siglas ambiguas dejan de meter ruido.

## 3. Scripts

### Bloque núcleo R (forma parte de todas las búsquedas)

```
TITLE-ABS-KEY (
  ( ( "non-functional" OR "non functional" OR nonfunctional OR quality OR NFR OR NFRs ) W/3 requirement* )
  OR "software requirement*" OR "requirements specification*"
  OR "requirement* classification" OR "PROMISE NFR" OR "PROMISE_exp"
)
AND TITLE-ABS-KEY ( classif* OR categori* )
```

### Filtros comunes (F)

```
AND PUBYEAR > 2016 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"cp" ) OR LIMIT-TO ( DOCTYPE,"re" ) OR LIMIT-TO ( DOCTYPE,"ch" ) )
AND ( LIMIT-TO ( LANGUAGE,"English" ) OR LIMIT-TO ( LANGUAGE,"Spanish" ) )
```

### S1 — Aumentación de datos y desbalance de clases

```
TITLE-ABS-KEY (
  ( ( "non-functional" OR "non functional" OR nonfunctional OR quality OR NFR OR NFRs ) W/3 requirement* )
  OR "software requirement*" OR "requirements specification*"
  OR "requirement* classification" OR "PROMISE NFR" OR "PROMISE_exp"
)
AND TITLE-ABS-KEY ( classif* OR categori* )
AND TITLE-ABS-KEY (
  "data augmentation" OR "text augmentation" OR "easy data augmentation" OR TextAttack OR TAOS
  OR "synthetic data" OR "synthetic sample*" OR oversampl* OR "over-sampling" OR resampl*
  OR SMOTE OR Tomek OR "class imbalance" OR "imbalanced data*" OR "imbalanced class*"
  OR "minority class*" OR "back translation" OR paraphras*
)
AND PUBYEAR > 2016 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"cp" ) OR LIMIT-TO ( DOCTYPE,"re" ) OR LIMIT-TO ( DOCTYPE,"ch" ) )
AND ( LIMIT-TO ( LANGUAGE,"English" ) OR LIMIT-TO ( LANGUAGE,"Spanish" ) )
```

### S2 — BERT y transformers

```
TITLE-ABS-KEY (
  ( ( "non-functional" OR "non functional" OR nonfunctional OR quality OR NFR OR NFRs ) W/3 requirement* )
  OR "software requirement*" OR "requirements specification*"
  OR "requirement* classification" OR "PROMISE NFR" OR "PROMISE_exp"
)
AND TITLE-ABS-KEY ( classif* OR categori* )
AND TITLE-ABS-KEY (
  BERT OR RoBERTa OR DistilBERT OR NoRBERT OR transformer* OR "pre-trained language model*"
  OR "pretrained language model*" OR "transfer learning" OR "fine tun*"
)
AND PUBYEAR > 2016 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"cp" ) OR LIMIT-TO ( DOCTYPE,"re" ) OR LIMIT-TO ( DOCTYPE,"ch" ) )
AND ( LIMIT-TO ( LANGUAGE,"English" ) OR LIMIT-TO ( LANGUAGE,"Spanish" ) )
```

### S3 — LLM como clasificador

```
TITLE-ABS-KEY (
  ( ( "non-functional" OR "non functional" OR nonfunctional OR quality OR NFR OR NFRs ) W/3 requirement* )
  OR "software requirement*" OR "requirements specification*"
  OR "requirement* classification" OR "PROMISE NFR" OR "PROMISE_exp"
)
AND TITLE-ABS-KEY ( classif* OR categori* )
AND TITLE-ABS-KEY (
  "large language model*" OR LLM OR LLMs OR GPT* OR ChatGPT OR "generative AI"
  OR Llama OR Gemma OR Mistral OR Claude OR "zero-shot" OR "few-shot"
  OR "in-context learning" OR prompt*
)
AND PUBYEAR > 2016 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"cp" ) OR LIMIT-TO ( DOCTYPE,"re" ) OR LIMIT-TO ( DOCTYPE,"ch" ) )
AND ( LIMIT-TO ( LANGUAGE,"English" ) OR LIMIT-TO ( LANGUAGE,"Spanish" ) )
```

### S4 — Ampliación con GitHub y auto-etiquetado

```
TITLE-ABS-KEY (
  ( ( "non-functional" OR "non functional" OR nonfunctional OR quality OR NFR OR NFRs ) W/3 requirement* )
  OR "software requirement*" OR "requirements specification*"
  OR "requirement* classification" OR "PROMISE NFR" OR "PROMISE_exp"
)
AND TITLE-ABS-KEY ( classif* OR categori* )
AND TITLE-ABS-KEY (
  GitHub OR "issue tracker*" OR "issue report*" OR "open source" OR "open-source"
  OR "semi-supervised" OR "self-training" OR "pseudo-label*" OR "active learning"
  OR "weak supervision" OR "dataset construction" OR "gold standard"
)
AND PUBYEAR > 2016 AND PUBYEAR < 2027
AND ( LIMIT-TO ( DOCTYPE,"ar" ) OR LIMIT-TO ( DOCTYPE,"cp" ) OR LIMIT-TO ( DOCTYPE,"re" ) OR LIMIT-TO ( DOCTYPE,"ch" ) )
AND ( LIMIT-TO ( LANGUAGE,"English" ) OR LIMIT-TO ( LANGUAGE,"Spanish" ) )
```

### S5 — Núcleo directo (competidores de la tesis)

En el historial de búsquedas de Scopus (*Search history → Combine queries*):

```
#1 AND ( #2 OR #3 )
```

donde #1 = S1, #2 = S2 y #3 = S3. Estos estudios se leen siempre en texto completo.

## 4. Procedimiento (para que el PRISMA sea reproducible)

1. Ejecutar S1, S2, S3 y S4 en este orden y **anotar el conteo de cada una** y la fecha.
2. Combinar `#1 OR #2 OR #3 OR #4` en el historial y exportar **ese** resultado en CSV, con todos los
   campos (*Citation, Bibliographical, Abstract & keywords, **References***). Este número es la casilla
   "Registros identificados" del PRISMA.
3. Ejecutar S5 y exportarlo aparte para marcar los competidores directos.
4. Si una exportación supera 2 000 registros (el límite del CSV de Scopus), dividirla por años.
5. Mover los CSV viejos a `SCUPUS/v1_2026-10-02/`, poner los nuevos en `SCUPUS/` y correr
   `python Articulos/analisis_scopus.py`. Eso regenera los conteos, el mapa y los candidatos.
6. Importar el CSV en Rayyan para el cribado.

Pásame los conteos y regenero las figuras y el texto del estado del arte y de la RSL. La
ecuación de Scopus de la RSL (Tabla de búsqueda) y su criterio de años (2017–2025 → 2017–2026)
deben actualizarse con estos scripts.

## 5. Correcciones a la lista de semillas recibida (bloques 3 y 4)

Verificadas contra Crossref / ACL Anthology y `RSL/referencias_nfr.bib`:

| Dato recibido | Correcto |
|---|---|
| Cleland-Huang et al. (2007), *RE'07*, pp. 360–369 | Revista **Requirements Engineering**, 12(2), **103–120**, doi 10.1007/s00766-007-0045-1 |
| Rubaidi et al. (2023), *Handling class imbalance … using SMOTE-Tomek* | Ese título no existe. El real es *Handling imbalance functional and non-functional software requirement classification based on machine learning algorithms*, **LNNS 2025**, pp. 199–209, tarea binaria. El precedente de **SMOTE-Tomek** en requerimientos es **Or (2025)**, arXiv 2501.06491. |
| Rahimi, M. et al. (2021), *Two-phase deep learning architecture…* | **Rahimi, N.**, Eassa, F. y Elrefaei, L. (2021). *One- and two-phase software requirement classification using ensemble deep learning*. **Entropy**, 23(10), 1264. |
| Morris, Elihashiv, Ghosh, Hudgins y Raza (2020) | Los autores son **Morris, Lifland, Yoo, Grigsby, Jin y Qi**. El título y las páginas 119–126 sí son correctos. |
| EDA, SMOTE, Batista, BERT, AugGPT | Correctos. |
