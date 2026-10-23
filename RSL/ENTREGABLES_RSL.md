# Lista de entregables para la RSL

Marca cada casilla cuando lo subas (`[ ]` → `[x]`). Todas las rutas son relativas a
`C:\Users\Lenovo\Documents\Tesis\`. Cuando termines un bloque, súbelo con:

```
cd C:\Users\Lenovo\Documents\Tesis
git add -A
git commit -m "Entregables RSL: <qué subiste>"
git push
```

> Las exportaciones de las bases de datos y los PDF **no se suben a GitHub** (están en el `.gitignore`
> por licencia). Basta con dejarlos en la carpeta indicada de esta laptop.

---

## 1. Búsquedas — ✅ cerrado

La RSL usa **solo Scopus** (S1–S4, octubre de 2026; 565 registros). Web of Science se descartó porque la
UPeU ya no tiene la suscripción. IEEE Xplore y ACM tampoco se buscan aparte: Scopus indexa sus
artículos (53 de los 145 incluidos son de IEEE y 5 de ACM). La justificación y la amenaza a la validez ya
están redactadas en `RSL\rsl.tex`.

---

## 2. Validación del cribado (kappa) — _responsables: Andrés y Cristian_

| ✔   | Archivo                                    | Carpeta      | Quién    |
| --- | ------------------------------------------ | ------------ | -------- |
| [ ] | `validacion_cribado_andres.xlsx` (lleno)   | `Articulos\` | Andrés   |
| [ ] | `validacion_cribado_cristian.xlsx` (lleno) | `Articulos\` | Cristian |

- Descarga: https://raw.githubusercontent.com/AlessandroPastor/research/main/Articulos/validacion_cribado_andres.xlsx
  y https://raw.githubusercontent.com/AlessandroPastor/research/main/Articulos/validacion_cribado_cristian.xlsx
- Cada uno por separado, sin mirar `cribado.csv` ni `incluidos.csv`.
- Cuando estén los dos, ejecutar: `python Articulos\validacion_cribado.py kappa`

---

## 3. Formato de la RSL — _responsable: Alessandro_

| ✔   | Archivo                                                                                | Carpeta      |
| --- | -------------------------------------------------------------------------------------- | ------------ |
| [ ] | Plantilla, rúbrica o guía de la RSL del curso o de la UPeU (PDF o Word), **si existe** | `RSL\`       |
| [ ] | Si no existe, escribir aquí: "No hay formato; usar IEEE"                               | este archivo |

---

## 4. Decisiones — _responsable: Alessandro (responder en el chat)_

| ✔   | Pregunta                                                                                                         | Respuesta |
| --- | ---------------------------------------------------------------------------------------------------------------- | --------- |
| [ ] | ¿Se queda la PR5 sobre el rigor de la evaluación? (ya está redactada en la RSL)                                  |           |
| [ ] | ¿Andrés y Cristian revisan una muestra del 20 % de la extracción y la calidad?                                   |           |

---

## 5. PDF de texto completo — _responsables: los tres_

Todo está en **`Articulos\PDF\INDICE_ARTICULOS.xlsx`**:

- Hoja **Estudios**: los 145 incluidos, con una X en la ecuación (S1–S4) que los encontró, el estado del
  PDF, el enlace "abrir" y la carpeta y el nombre exactos con que hay que guardarlo.
- Hoja **Por ecuación**: los mismos estudios agrupados por S1, S2, S3 y S4.
- Hoja **Ecuaciones**: el texto completo de cada ecuación para pegar en Scopus.

| Estado del PDF               | Cuántos | Cómo                                                                       |
| ---------------------------- | ------- | -------------------------------------------------------------------------- |
| Descargado                   | 67      | Ya extraídos en la RSL (incluye los 11 de ScienceDirect y 25 bajados por Claude). |
| Acceso abierto (navegador)   | 13      | ACM, Wiley y repositorios bloquean la descarga automática: clic en "abrir" → botón PDF desde el navegador. |
| De pago (sin suscripción)    | 61      | IEEE, Springer, etc. Probar con el autor (ResearchGate) o pedirlo por correo. Si no, quedan como "sin acceso" en el PRISMA. |
| Sin DOI                      | 4       | El enlace abre Google Scholar con el título.                               |

Para volver a intentar la descarga automática de los de acceso abierto: `python Articulos\descargar_abiertos.py`.

| ✔   | Qué                                                                            | Dónde                                    |
| --- | ------------------------------------------------------------------------------ | ---------------------------------------- |
| [ ] | Cada PDF guardado en la carpeta y con el **nombre exacto** que indica el Excel | `Articulos\PDF\<carpeta>\`               |
| [ ] | Avisar a Claude: extrae los nuevos y regenera la RSL                           | `python Articulos\resultados_rsl.py`     |

Para actualizar el Excel después de descargar: `python Articulos\indice_articulos.py`.

## Resumen de responsables

| Quién          | Qué                                                                                       |
| -------------- | ----------------------------------------------------------------------------------------- |
| **Alessandro** | Bloques 3 y 4; los 12 PDF de ScienceDirect                                                |
| **Andrés**     | Planilla del kappa (bloque 2) y parte de los PDF de acceso abierto                        |
| **Cristian**   | Planilla del kappa (bloque 2) y parte de los PDF de acceso abierto                        |
| **Claude**     | Extracción y calidad de cada PDF nuevo, tablas de resultados y redacción de la RSL        |
