# Criterios de inclusión y exclusión (versión 2, 2026-10-09)

Se aplican a los registros de las búsquedas S1–S4 de Scopus (ver `FORMULAS_BUSQUEDA_SCOPUS.txt`).
Las decisiones registro por registro están en `cribado.csv`, generado por `analisis_scopus.py` a partir de
`cribado_decisiones.py`.

## Criterios de inclusión (deben cumplirse todos)

| Código | Criterio | Cómo se verifica |
|---|---|---|
| **CI1** | Estudio **primario** que **clasifica automáticamente texto de requerimientos** en tipos de requerimiento o en atributos de calidad: FR/NFR, subclases de NFR, seguridad, privacidad, usabilidad, ética, etc. También cuenta el texto de usuarios (reseñas, solicitudes, issues) **si las clases son tipos de requerimiento o atributos de calidad**. | Título y resumen |
| **CI2** | Usa aprendizaje automático, aprendizaje profundo, transformers o LLM. | Resumen |
| **CI3** | Reporta una **evaluación empírica** cuantitativa (exactitud, precisión, exhaustividad, F1…). | Resumen y, después, texto completo |
| **CI4** | Publicado entre 2017 y 2026, en inglés o español, como artículo, ponencia, revisión o capítulo. | Aplicado en la ecuación de búsqueda |

## Criterios de exclusión (basta uno)

| Código | Criterio | Ejemplos reales del cribado |
|---|---|---|
| **CE1** | **Fuera del dominio de software.** La palabra *requirement* o *quality* aparece con otro sentido. | Control de calidad en manufactura, imágenes médicas, redes 5G, diseño de productos |
| **CE2** | **Software o ingeniería de requerimientos, pero otra tarea**, o clases que no son tipos de requerimiento. | Ambigüedad, trazabilidad, generación de requisitos o de historias, priorización, riesgo, NER, pruebas, bugs/feature requests, sentimiento, sectores de *CrowdRE*, dimensiones de sostenibilidad |
| **CE3** | **Sin evaluación empírica.** | Capítulos tutoriales, propuestas de visión, artículos de dataset sin experimentos |
| **CE4** | **Estudio secundario** (revisión, mapeo, survey). No entra en la síntesis de estudios primarios, pero se usa como contexto. | Revisiones de LLM en RE, mapeos de IA en clasificación de requerimientos |
| **CE5** | **Duplicado**, o versión resumida o extendida de otro registro incluido. | Dos versiones del mismo artículo con títulos casi idénticos |

**Regla de duda:** si el título y el resumen no permiten decidir, el registro **pasa a texto completo**
(práctica estándar de PRISMA 2020).

## Resultado del cribado por título y resumen

| Etapa | n |
|---|---|
| Registros identificados (S1 + S2 + S3 + S4) | 565 |
| Duplicados entre búsquedas | 131 |
| Registros únicos cribados | 434 |
| Excluidos CE1 (otro dominio) | 142 |
| Excluidos CE2 (otra tarea) | 129 |
| Excluidos CE3 (sin evaluación) | 4 |
| Excluidos CE5 (duplicado/resumen) | 2 |
| Estudios secundarios (CE4, contexto) | 12 |
| **Incluidos para lectura de texto completo** | **145** |

**Pendiente (elegibilidad):** leer el texto completo de los 145 y aplicar de nuevo CI3; también hay que
confirmar en el texto completo los que pasaron por la regla de duda. En el PRISMA se anotan los que no se
puedan obtener y los excluidos en esta etapa.

**Validación (sin Rayyan), con dos revisores:** Andrés y Cristian revisan a ciegas y por separado
su propia planilla (`validacion_cribado_andres.xlsx` y `validacion_cribado_cristian.xlsx`). Cada una tiene
los 145 incluidos y el 20 % de los excluidos (58), en un orden aleatorio distinto y sin las decisiones del
cribado inicial (asistido por IA). Cuando ambos terminen:

    python Articulos/validacion_cribado.py kappa

El script calcula el kappa de Cohen por pares y el kappa de Fleiss de los tres evaluadores, y guarda los
desacuerdos con la decisión por mayoría en `desacuerdos_cribado.csv`. Los valores se copian en
`\kappaFleiss` y `\kappaCohen` al inicio de `EstadoArte/EstadoArte_NFR.tex`.
