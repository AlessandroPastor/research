# Lista de entregables para la RSL

Marca cada casilla cuando lo subas (`[ ]` → `[x]`). Todas las rutas son relativas a
`C:\Users\Lenovo\Documents\Tesis\`. Cuando termines un bloque, súbelo con:

```
cd C:\Users\Lenovo\Documents\Tesis
git add -A
git commit -m "Entregables RSL: <qué subiste>"
git push
```

> Las exportaciones de las bases de datos **no se suben a GitHub** (están en el `.gitignore` por
> licencia). Basta con dejarlas en la carpeta indicada de esta laptop.

---

## 1. Búsquedas en Web of Science, IEEE Xplore y ACM — *responsable: Alessandro*

Fórmulas y pasos de exportación: `Articulos\FORMULAS_BUSQUEDA_WOS_IEEE_ACM.txt`.
Hacer las 12 búsquedas **el mismo día**.

| ✔ | Archivo | Carpeta | Cómo exportarlo |
|---|---|---|---|
| [ ] | `W1.xls` | `Articulos\WOS\` | Excel → *Full Record* |
| [ ] | `W2.xls` | `Articulos\WOS\` | Excel → *Full Record* |
| [ ] | `W3.xls` | `Articulos\WOS\` | Excel → *Full Record* |
| [ ] | `W4.xls` | `Articulos\WOS\` | Excel → *Full Record* |
| [ ] | `I1.csv` | `Articulos\IEEE\` | CSV → *Citation and Abstract* |
| [ ] | `I2.csv` | `Articulos\IEEE\` | CSV → *Citation and Abstract* |
| [ ] | `I3.csv` | `Articulos\IEEE\` | CSV → *Citation and Abstract* |
| [ ] | `I4.csv` | `Articulos\IEEE\` | CSV → *Citation and Abstract* |
| [ ] | `A1.bib` (y `A1_p2.bib`… si hay más páginas) | `Articulos\ACM\` | BibTeX, 50 por página |
| [ ] | `A2.bib` | `Articulos\ACM\` | BibTeX |
| [ ] | `A3.bib` | `Articulos\ACM\` | BibTeX |
| [ ] | `A4.bib` | `Articulos\ACM\` | BibTeX |
| [ ] | `conteos.txt` (la tabla de abajo, llena) | `Articulos\` | Bloc de notas |

Contenido de `conteos.txt`:

```
Fecha de búsqueda: __/__/2026

        Eje 1   Eje 2   Eje 3   Eje 4
WoS     W1=___  W2=___  W3=___  W4=___
IEEE    I1=___  I2=___  I3=___  I4=___
ACM     A1=___  A2=___  A3=___  A4=___

Errores o cambios en alguna fórmula (copiar el mensaje exacto):
```

---

## 2. Validación del cribado (kappa) — *responsables: Andrés y Cristian*

| ✔ | Archivo | Carpeta | Quién |
|---|---|---|---|
| [ ] | `validacion_cribado_andres.xlsx` (lleno) | `Articulos\` | Andrés |
| [ ] | `validacion_cribado_cristian.xlsx` (lleno) | `Articulos\` | Cristian |

- Descarga: https://raw.githubusercontent.com/AlessandroPastor/research/main/Articulos/validacion_cribado_andres.xlsx
  y https://raw.githubusercontent.com/AlessandroPastor/research/main/Articulos/validacion_cribado_cristian.xlsx
- Cada uno por separado, sin mirar `cribado.csv` ni `incluidos.csv`.
- Cuando estén los dos, ejecutar: `python Articulos\validacion_cribado.py kappa`

---

## 3. Formato de la RSL — *responsable: Alessandro*

| ✔ | Archivo | Carpeta |
|---|---|---|
| [ ] | Plantilla, rúbrica o guía de la RSL del curso o de la UPeU (PDF o Word), **si existe** | `RSL\` |
| [ ] | Si no existe, escribir aquí: "No hay formato; usar IEEE" | este archivo |

---

## 4. Decisiones — *responsable: Alessandro (responder en el chat)*

| ✔ | Pregunta | Respuesta |
|---|---|---|
| [ ] | ¿Se agrega la PR5 sobre calidad de la evidencia ("¿con qué rigor se evalúan los métodos contra el desbalance?")? | |
| [ ] | ¿La evaluación de calidad la hace Claude con el texto completo y Andrés y Cristian revisan una muestra? | |

---

## 5. PDF de texto completo — *responsables: los tres*

Claude ya descargó los de acceso abierto que permiten descarga automática (33) en
`Articulos\PDF_semillas` … `07_revisiones`. Faltan **135**, listados en
**`Articulos\PDF\FALTANTES.xlsx`** (con enlaces clicables):

| Acceso | Cuántos | Cómo |
|---|---|---|
| Abierto | 55 | Clic en "Abrir" → botón PDF. Gratis, sin cuenta. **Empezar por estos.** |
| De pago | 74 | Entrar primero con la cuenta de la biblioteca de la UPeU y luego "Abrir". |
| Sin DOI | 6 | El enlace abre Google Scholar con el título. |

| ✔ | Qué | Dónde |
|---|---|---|
| [ ] | Cada PDF guardado en la carpeta y con el **nombre exacto** que indica el Excel | `Articulos\PDF\<carpeta>\` |
| [ ] | Columna "¿Descargado?" marcada en el Excel | `Articulos\PDF\FALTANTES.xlsx` |

Sugerencia para repartir: Alessandro → `03_aumentacion`, `01_semillas`, `02_trabajos_base`;
Andrés → `04_bert_transformers`; Cristian → `05_llm`, `06_ml_dl_clasico`, `07_revisiones`.

## Resumen de responsables

| Quién | Qué |
|---|---|
| **Alessandro** | Bloques 1, 3 y 4, y repartir el bloque 5 |
| **Andrés** | Planilla del kappa (bloque 2) y parte de los PDF |
| **Cristian** | Planilla del kappa (bloque 2) y parte de los PDF |
| **Claude** | PDF de acceso abierto, protocolo, lista de calidad, formulario de extracción y redacción de la RSL |
