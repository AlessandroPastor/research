# Mapas bibliométricos con VOSviewer

Archivos de entrada (en esta carpeta):
- `incluidos_scopus.csv`: los 145 estudios incluidos, en formato Scopus. Se regenera con
  `python Articulos/preparar_vosviewer.py`.
- `tesauro_palabras_clave.txt`: une sinónimos (NFR / non-functional requirements, LLM / large language
  models…) y descarta términos genéricos de indexación.

Se generan **dos mapas**. Ambos se citan como elaborados con VOSviewer (van Eck y Waltman, 2010).

---

## 0. Instalar VOSviewer (una sola vez)

1. Entrar a https://www.vosviewer.com → **Download** → *VOSviewer for Microsoft Windows* (archivo .zip).
2. Descomprimir el .zip (por ejemplo, en `C:\VOSviewer`) y abrir **VOSviewer.exe**.
   Tu equipo ya tiene Java 17, que es lo que necesita.

---

## Mapa A — Co-ocurrencia de palabras clave (temas y su evolución)

1. **Create** → *Create a map based on bibliographic data* → **Next**.
2. *Read data from bibliographic database files* → **Next**.
3. Pestaña **Scopus** → elegir `Articulos\vosviewer\incluidos_scopus.csv` → **Next**.
4. *Type of analysis:* **Co-occurrence**. *Unit of analysis:* **All keywords**.
   *Counting method:* **Full counting** → **Next**.
5. *VOSviewer thesaurus file:* elegir `Articulos\vosviewer\tesauro_palabras_clave.txt` → **Next**.
6. *Minimum number of occurrences of a keyword:* **5** → **Next** → dejar todos marcados → **Finish**.
7. En el panel derecho, pestaña **Analysis**: *Resolution* = **1.00**, *Min. cluster size* = **5**
   → **Update**.
8. Exportar **dos vistas**:
   - Pestaña **Network Visualization** → **Screenshot** → *Save* → formato **PNG**, opción
     *Scaling* **400 %** → guardar como `recursos\vos_palabras_red.png`.
   - Pestaña **Overlay Visualization** (colorea por año promedio de publicación) → **Screenshot** →
     *Save* → PNG, 400 % → guardar como `recursos\vos_palabras_anios.png`.
9. **Guardar los datos del mapa** (los necesito para describir los clústeres con exactitud):
   **Save** → *Save map file* → `Articulos\vosviewer\palabras_map.txt`
   y *Save network file* → `Articulos\vosviewer\palabras_network.txt`.

## Mapa B — Co-citación de referencias (trabajos base del área)

1. **Create** → *Create a map based on bibliographic data* → *Read data from bibliographic database
   files* → pestaña **Scopus** → el mismo `incluidos_scopus.csv` → **Next**.
2. *Type of analysis:* **Co-citation**. *Unit of analysis:* **Cited references**.
   *Counting method:* **Full counting** → **Next**.
3. *Minimum number of citations of a cited reference:* **10** → **Next** → **Finish**.
   (Si salen menos de 20 referencias, volver y usar **8**.)
4. Pestaña **Network Visualization** → **Screenshot** → *Save* → PNG, 400 % →
   `recursos\vos_cocitacion.png`.
5. **Save** → *Save map file* → `Articulos\vosviewer\cocitacion_map.txt`
   y *Save network file* → `Articulos\vosviewer\cocitacion_network.txt`.

---

## Qué enviar

| Archivo | Carpeta |
|---|---|
| `vos_palabras_red.png`, `vos_palabras_anios.png`, `vos_cocitacion.png` | `recursos\` |
| `palabras_map.txt`, `palabras_network.txt`, `cocitacion_map.txt`, `cocitacion_network.txt` | `Articulos\vosviewer\` |

Con esos archivos se reemplaza el mapa actual del estado del arte, se agrega el mapa de temas por año y
se redactan los clústeres a partir de los datos reales del mapa.

**Consejos para que se vea profesional:**
- Antes del screenshot, ajustar la ventana para que el mapa quede centrado y sin etiquetas cortadas.
- Si hay etiquetas que se superponen, en **Visualization** bajar *Labels → Size variation* o subir
  *Scale*.
- No cambiar los colores por defecto: son los que el jurado reconoce de VOSviewer.
